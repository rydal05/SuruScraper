import time
from bs4 import BeautifulSoup
import requests
import sqlite3

import suruScraper.config as _G

from suruScraper.database import get_prefixes
from suruScraper.notify import send_notification # temporary kde 

def suru_scrape_task(): # refactoring to be single use
	with sqlite3.connect('suru.db') as conn: # open database
		cursor, items = getCursGetItems(conn)
		for item_id, url, original_name in items: #for loop iterating over all items in db
			try:
				soup = getSoup(url)
				if not soup: continue
				name = updateName(original_name, soup,cursor,item_id)
				checkIfExists(soup, name) # first and foremost we do our check to see whether it's for sale or not
				conn.commit()
				time.sleep(_G.waitTime)
			except Exception as e:
				print(f"Error scraping {url}:{e}")

def updateName(original_name:str, soup:BeautifulSoup, cursor:sqlite3.Cursor, item_id):
	name = original_name # Update outdated names
	
	if original_name == "BLANK": #update seeded names and names with no preset naming
		title_tag = soup.find("h1", class_="title_product")
		if title_tag:
			name = title_tag.text.strip()
		for prefix in get_prefixes():
			name = name.removeprefix(prefix).strip()
		cursor.execute("UPDATE wishlist SET name = ? WHERE id = ?", (name, item_id))

	return name

def getSoup(url:str):
	response = requests.get(url, timeout=10) #attempt to call into website
	if response.status_code != 200: return None #link broken = continue
	return BeautifulSoup(response.content, "lxml") #lxml read over site

def checkIfExists(soup:BeautifulSoup,name:str): # currently only supports surugaya but I will eventually expand this to check cases for unique websites to allow for more than just Surugaya scraping
	addToCartBtn = soup.find("button",id='add-cart-btn') # for surugaya specifically, checks if the add to cart button exists (most reliable way to tell if a product is in stock)

	if addToCartBtn:
		price_input = soup.find("input", class_="priceValue")
		price_val = price_input["value"] if price_input else "Unknown"
		send_notification("ITEM IN STOCK",name + " at " + price_val) #TODO: Have price format thousands I.E 1,000,000
		print(f"{name}: AVAILABLE @ ¥{price_val}") #TODO: add live USD conversion to spit out somewhere here
	else:
		print(name + ": PRODUCT UNAVAILABLE")

def scrapeResponse(): # not even sure what im gonna use this for
	pass

def getCursGetItems(conn: sqlite3.Connection):
	cursor = conn.cursor()
	items = cursor.execute("SELECT id, url, name FROM wishlist").fetchall() #get entire db
	return cursor, items