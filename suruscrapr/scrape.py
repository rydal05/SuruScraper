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

			if ".com" in url:
				name, msrp, current_price, category, media_format = suru_com_scrape(soup)
			elif ".jp" in url:
				name, msrp, current_price, category, media_format = suru_jp_scrape(soup)
			# 3: pull item info from page and propagate database TODO: start pulling high level category (I.e, Video software, Music software, Toy hobby (maybe even trim subcategory or do subsorts))
			
			propagate_db(name, msrp, current_price, category, media_format)

			# 4: check if item is in stock (split out functions for different sites and whatever)
			checkIfExists(soup, name,db, item_id)

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

#TODO: needs refactoring, should be made more clear
def checkIfExists(soup:BeautifulSoup,name:str,db,item_id):
	addToCartBtn = soup.find("button",id='add-cart-btn') 
	if addToCartBtn:
		price_input = soup.find("input", class_="priceValue")
		price_val = price_input["value"] if price_input else "Unknown" 
		concatPrice = f"¥{price_val}"
		print(f"{name}: AVAILABLE @ {price_val}")
		curDate = datetime.now().strftime("%m/%d/%Y %H:%M")
		db.execute(
       "UPDATE wishlist SET price = ?, lastSeenDateTime = ? WHERE id = ?",
       (concatPrice, curDate, item_id)
   )
	else:
		print(name + ": PRODUCT UNAVAILABLE")

# DONE:
def intl_name(soup:BeautifulSoup):
	nametag = soup.find("meta", property="og:title")
	meta_name = nametag.get("content")
	
	return meta_name

# FIXME:
def intl_format(soup:BeautifulSoup):
	# 1. Check if media tag is available
	mediatag = soup.find("span", class_="text-gray-dark text-nowrap") #TODO: needs something more specific to grab at, unreliable
	next_sib = mediatag.find_next_sibling()

	if next_sib and isinstance(next_sib, str):
		media_format = next_sib.strip()
		return media_format
	
	return None

	
# TESTME:
def intl_price(soup:BeautifulSoup):
	addToCartBtn = soup.find("button",id='add-cart-btn') 

	if not addToCartBtn: return None # Item must be in stock to check for price

	price_input = soup.find("input", class_="priceValue")
	price_val = price_input["value"]

	pass

def intl_category(soup:BeautifulSoup):
	category = soup.find("span", class_="text-gray-dark text-nowrap") #TODO: see above

	# skip whitespace
	# check first category tag (Doujin software, Doujin magazine, etc)

	return None

def intl_OG_price(soup:BeautifulSoup):
	# 1. check for label with text "Listed Price:"
	listed_label = soup.find("label", class_="m1-2 price-suggest")
	if not listed_label: return None # Item must be in stock to check for price
	# 2. check following div afterwards
	# 3. trim "JPY" from the field
	# 4. return int
	pass


def jp_name(soup:BeautifulSoup):
	pass

def jp_OG_price(soup:BeautifulSoup):
	pass

def jp_price(soup:BeautifulSoup):
	pass

def jp_category(soup:BeautifulSoup):
	pass

def jp_format(soup:BeautifulSoup):
	pass

def suru_com_scrape(soup:BeautifulSoup):
	name = intl_name(soup)
	msrp = intl_OG_price(soup)
	current_price = intl_price(soup)
	category = intl_category(soup)
	media_format = intl_format(soup)

	return name, msrp, current_price,category, media_format

def suru_jp_scrape(soup:BeautifulSoup):
	name = jp_name(soup)
	msrp = jp_OG_price(soup)
	current_price = jp_price(soup)
	category = jp_category(soup)
	media_format = jp_format(soup)

	return name, msrp, current_price, category, media_format

def propagate_db(name, msrp, current_price, category, media_format):
	pass