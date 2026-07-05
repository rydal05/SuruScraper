from pathlib import Path

from bs4 import BeautifulSoup
import requests

import time

import sqlite3
from datetime import datetime

from flask import current_app, g

from suruscrapr.db import get_prefixes
from suruscrapr.db import get_db, get_all_items

from headers_generator import generate_headers

import configparser

import json 
config = configparser.ConfigParser()
config.read('config.ini')

c_wait = float(config['settings']['waitTime'])

import os

#TODO: potentially implement header generation or at least some variation that doesn't use a static variant

def suru_scrape_task(): #TODO: also need to implement cleaner usage
	db = get_db()

	items = db.execute("SELECT id, url, name FROM wishlist").fetchall()

	for item_id, url, original_name in items:
		time.sleep(c_wait)

		try:
			soup = getSoup(url) # 1: pull page

			if not soup: continue # 2: check if pull successful

			name, price, availability, release_date, description, image = suruSchemaScrape(soup)

			# 5: commit new information to database
			db.commit()
		except Exception as e:
			print(f"Error scraping {url}:{e}",flush=True)


def updateName(original_name:str, soup:BeautifulSoup, db, item_id): #TODO: should be made cleaner to read
	name = original_name

	if original_name == "BLANK": # TODO: change detecting if the item name was blank to utilizing the clean boolean
		title_tag = soup.find("h1", class_="title_product") # probably also move checking these outside the function in the first place, or use a function to do table value checks
		if title_tag:
			name = title_tag.text.strip()
		for prefix in get_prefixes():
			name = name.removeprefix(prefix).strip()
		db.execute("UPDATE wishlist SET name = ?, cleaned = 1 WHERE id = ?", (name, item_id))

	return name

# DONE: 
def getSoup(url:str):
	spoof = generate_headers()
	
	response = requests.get(url, timeout=10, headers=spoof)
	if response.status_code != 200:
		print(f"FAILED TO LOCATE SOUP: {response.status_code}") 
		return None
	return BeautifulSoup(response.content, "lxml")

def suruSchemaScrape(soup:BeautifulSoup): # Compliant with surugaya US and JP site
	scripts = soup.find_all("script", type="application/ld+json")
	
	valid_script = None

	for script_tag in scripts: # multiple script tags contain json information the one we're looking for has a particular variable assignment that we iterate for
		try:
			json_data = script_tag.string
			parsed_json = json.loads(json_data)

			if "Product" in str(parsed_json.get("brand", {})):
				valid_script = parsed_json
				break
		except json.JSONDecodeError:
			print("Error decoding json")

	if valid_script == None: return None

	name = parsed_json.get('name')
	price = parsed_json['offers'].get('price')
	availability = parsed_json['offers'].get('availability') # outputs as "https://schema.org/OutOfStock" or "https://schema.org/InStock"

	release_date = parsed_json.get('releaseDate') if 'releaseDate' in parsed_json else None

	description = parsed_json.get('description')
	image = parsed_json.get('image')


	return name, price, availability, release_date, description, image
	# head > script (type = application/ld+json") > name