import time
from datetime import datetime

import requests
from bs4 import BeautifulSoup

import json 
import configparser

from suruscrapr.headers_generator import generate_headers
from suruscrapr.db import get_db, update_item

def suru_scrape_task(): #TODO: also need to implement cleaner usage
	config = configparser.ConfigParser()
	config.read('config.ini')
	C_WAIT = float(config['settings']['waitTime'])

	db = get_db()

	items = db.execute("SELECT id, url FROM wishlist").fetchall()

	for id, url in items:
		time.sleep(C_WAIT)
		try:
			soup = getSoup(url) # 1: pull page

			if not soup: continue # 2: check if pull successful

			SuruID, name, price, availability, dateLastSeen, description, image = suruSchemaScrape(soup)
			print(f"Current item stats: {SuruID, name, price, availability, dateLastSeen, description, image}")
			print(f"We are inserting it into location {id}")
			update_item(id, SuruID, name, price, availability, dateLastSeen, description, image)
			
		except Exception as e:
			print(f"Error scraping {url}:{e}",flush=True)
			break
	db.close()

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
	parsed_json = {}

	for script_tag in scripts: # multiple script tags contain json information the one we're looking for has a particular variable assignment that we iterate for
		try:
			json_data = script_tag.string
			parsed_json = json.loads(json_data)

			if "Product" in str(parsed_json.get("@type", {})):
				valid_script = parsed_json
				break
		except json.JSONDecodeError:
			print("Error decoding json")

	if valid_script == None: print("RETURNING: INVALID SCRIPT"); return None

	SuruID = parsed_json.get('productID') if 'productID' in parsed_json else None
	name = parsed_json.get('name') if 'name' in parsed_json else None
	price = parsed_json['offers']['price'] #offers is nested dict
	availability = ['offers']['availability'] if 'availability' in parsed_json else None # outputs as "https://schema.org/OutOfStock" or "https://schema.org/InStock"
	dateLastSeen = None

	if availability:
		curDate = datetime.now().strftime("%m/%d/%Y %H:%M")
		dateLastSeen = curDate
	
	release_date = parsed_json.get('releaseDate') if 'releaseDate' in parsed_json else None

	description = parsed_json.get('description') if 'description' in parsed_json else None
	image = parsed_json.get('image') if 'image' in parsed_json else None


	return SuruID, name, price, availability, dateLastSeen, description, image
	# head > script (type = application/ld+json") > name