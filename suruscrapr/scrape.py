from pathlib import Path

from bs4 import BeautifulSoup
import requests

import time

import sqlite3
from datetime import datetime

from flask import current_app, g

from suruscrapr.db import get_prefixes
from suruscrapr.db import get_db, get_all_items

import configparser
config = configparser.ConfigParser()
config.read('config.ini')

c_wait = float(config['settings']['waitTime'])

import os

#TODO: potentially implement header generation or at least some variation that doesn't use a static variant
headers = { 
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:152.0) Gecko/20100101 Firefox/152.0",
	"Accept": "image/avif,image/webp,image/png,image/svg+xml,image/*;q=0.8,*/*;q=0.5",
	"Accept-Language": "en-US,en;q=0.9",
	"Accept-Encoding": "gzip, deflate, br, zstd",
	"Sec-GPC": "1",
	"Connection": "keep-alive",
}

def suru_scrape_task(): #TODO: also need to implement cleaner usage
	db = get_db()

	items = db.execute("SELECT id, url, name FROM wishlist").fetchall()

	for item_id, url, original_name in items:
		time.sleep(c_wait)

		try:
			soup = getSoup(url) # 1: pull page

			if not soup: continue # 2: check if pull successful
			# 2.5: branch depending on which site we're on
			
			# 3: pull item info from page and propagate database TODO: start pulling high level category (I.e, Video software, Music software, Toy hobby (maybe even trim subcategory or do subsorts))
			name = scrape_name(soup)
			listed_price = scrape_OG_price(soup)
			current_price = scrape_price(soup)
			category = scrape_category(soup)
			media_format = scrape_format(soup)

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
	response = requests.get(url, timeout=10, headers=headers)
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
def scrape_name(soup:BeautifulSoup):
	nametag = soup.find("meta", property="og:title")
	meta_name = nametag.get("content")
	
	return meta_name

# FIXME:
def scrape_format(soup:BeautifulSoup):
	# 1. Check if media tag is available
	mediatag = soup.find("span", class_="text-gray-dark text-nowrap") #TODO: needs something more specific to grab at, unreliable
	next_sib = mediatag.find_next_sibling()

	if next_sib and isinstance(next_sib, str):
		media_format = next_sib.strip()
		return media_format
	
	return None

	
# TESTME:
def scrape_price(soup:BeautifulSoup):
	addToCartBtn = soup.find("button",id='add-cart-btn') 

	if not addToCartBtn: return None # Item must be in stock to check for price

	price_input = soup.find("input", class_="priceValue")
	price_val = price_input["value"]

	pass

def scrape_category(soup:BeautifulSoup):
	category = soup.find("span", class_="text-gray-dark text-nowrap") #TODO: see above

	# skip whitespace
	# check first category tag (Doujin software, Doujin magazine, etc)

	return None

def scrape_OG_price(soup:BeautifulSoup):
	# 1. check for label with text "Listed Price:"
	listed_label = soup.find("label", class_="m1-2 price-suggest")
	if not listed_label: return None # Item must be in stock to check for price
	# 2. check following div afterwards
	# 3. trim "JPY" from the field
	# 4. return int
	pass
