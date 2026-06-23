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

headers = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:152.0) Gecko/20100101 Firefox/152.0",
	"Accept": "image/avif,image/webp,image/png,image/svg+xml,image/*;q=0.8,*/*;q=0.5",
	"Accept-Language": "en-US,en;q=0.9",
	"Accept-Encoding": "gzip, deflate, br, zstd",
	"Sec-GPC": "1",
	"Connection": "keep-alive",
}


def suru_scrape_task():
	db = get_db()

	print("Starting scrape task",flush=True)
	items = db.execute("SELECT id, url, name FROM wishlist").fetchall()
	for item_id, url, original_name in items:
		time.sleep(c_wait)
		try:
			print("Enumerating scrape task " + url,flush=True)
			soup = getSoup(url)
			
			if not soup: continue
			
			name = updateName(original_name, soup,db,item_id)
			checkIfExists(soup, name,db, item_id)
			db.commit()
		except Exception as e:
			print(f"Error scraping {url}:{e}",flush=True)


def updateName(original_name:str, soup:BeautifulSoup, db, item_id):
	name = original_name

	if original_name == "BLANK":
		title_tag = soup.find("h1", class_="title_product")
		if title_tag:
			name = title_tag.text.strip()
		for prefix in get_prefixes():
			name = name.removeprefix(prefix).strip()
		db.execute("UPDATE wishlist SET name = ?, cleaned = 1 WHERE id = ?", (name, item_id))

	return name


def getSoup(url:str):
	response = requests.get(url, timeout=10, headers=headers)
	if response.status_code != 200:
		print(f"FAILED TO LOCATE SOUP: {response.status_code}") 
		return None
	return BeautifulSoup(response.content, "lxml")


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
		#here
	else:
		print(name + ": PRODUCT UNAVAILABLE")