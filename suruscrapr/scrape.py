from pathlib import Path

from bs4 import BeautifulSoup
import requests

import time

import sqlite3
from datetime import datetime

from flask import current_app, g

from suruscrapr.db import get_prefixes
from suruscrapr.db import get_db, get_all_items
#from notify import send_notification # temporary kde 

headers = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:152.0) Gecko/20100101 Firefox/152.0",
	"Accept": "image/avif,image/webp,image/png,image/svg+xml,image/*;q=0.8,*/*;q=0.5",
	"Accept-Language": "en-US,en;q=0.9",
	"Accept-Encoding": "gzip, deflate, br, zstd",
	"Sec-GPC": "1",
	"Connection": "keep-alive",
}

def suru_scrape_task(): # refactoring to be single use
	db = get_db()

	print("Starting scrape task",flush=True)
	items = db.execute("SELECT id, url, name FROM wishlist").fetchall()
	for item_id, url, original_name in items: #for loop iterating over all items in db
		time.sleep(3.0) #config.waittime
		try:
			print("Enumerating scrape task " + url,flush=True)
			soup = getSoup(url)
			
			if not soup: continue
			
			name = updateName(original_name, soup,db,item_id)
			checkIfExists(soup, name,db, item_id) # first and foremost we do our check to see whether it's for sale or not
			db.commit()
		except Exception as e:
			print(f"Error scraping {url}:{e}",flush=True)
	
	

def updateName(original_name:str, soup:BeautifulSoup, db, item_id):
	name = original_name # Update outdated names

	if original_name == "BLANK": #update seeded names and names with no preset naming
		title_tag = soup.find("h1", class_="title_product")
		if title_tag:
			name = title_tag.text.strip()
		for prefix in get_prefixes():
			name = name.removeprefix(prefix).strip()
		db.execute("UPDATE wishlist SET name = ?, cleaned = 1 WHERE id = ?", (name, item_id))

	return name

def getSoup(url:str):
	response = requests.get(url, timeout=10, headers=headers) #attempt to call into website
	if response.status_code != 200:
		print(f"FAILED TO LOCATE SOUP: {response.status_code}") 
		return None #link broken = continue
	return BeautifulSoup(response.content, "lxml") #lxml read over site

def checkIfExists(soup:BeautifulSoup,name:str,db,item_id): # currently only supports surugaya but I will eventually
	#expand this to check cases for unique websites to allow for more than just Surugaya scraping
	addToCartBtn = soup.find("button",id='add-cart-btn') # for surugaya specifically, checks if the add
	#to cart button exists (most reliable way to tell if a product is in stock)

	if addToCartBtn:
		price_input = soup.find("input", class_="priceValue")
		price_val = price_input["value"] if price_input else "Unknown"
		concatPrice = f"¥{price_val}"
		#send_notification("ITEM IN STOCK",name + " at " + price_val) #TODO: Have price format thousands
		# #I.E 1,000,000, also change this out for the email notifier whenever I do that 
		print(f"{name}: AVAILABLE @ {price_val}") #TODO: add live USD conversion to spit out somewhere
		curDate = datetime.now().strftime("%m/%d/%Y %H:%M")
		db.execute(
       "UPDATE wishlist SET price = ?, lastSeenDateTime = ? WHERE id = ?",
       (concatPrice, curDate, item_id)
   )
		#here
	else:
		print(name + ": PRODUCT UNAVAILABLE")