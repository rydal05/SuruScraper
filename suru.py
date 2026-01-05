from bs4 import BeautifulSoup
import requests
from flask import Flask
import sys
import time

print(sys.executable)

surugayaPages = [
	'https://www.suruga-ya.com/en/product/ZHORE50831',
	'https://www.suruga-ya.com/en/product/ZHORE138875',
	'https://www.suruga-ya.com/en/product/ZHORE70652',
	'https://www.suruga-ya.com/en/product/ZHORE29719',
	'https://www.suruga-ya.com/en/product/ZHORE79987',
	'https://www.suruga-ya.com/en/product/ZHORE79987',
	'https://www.suruga-ya.com/en/product/ZHORE80042',
	'https://www.suruga-ya.com/en/product/ZHORE229720',
	'https://www.suruga-ya.com/en/product/ZHORE138862',
	'https://www.suruga-ya.com/en/product/ZHORE55361',
	'https://www.suruga-ya.com/en/product/ZHORE9659',
	'https://www.suruga-ya.com/en/product/186011708',
	'https://www.suruga-ya.com/en/product/186023385',
	'https://www.suruga-ya.com/en/product/186023384',
	'https://www.suruga-ya.com/en/product/186147823',
	'https://www.suruga-ya.com/en/product/186118307',
	'https://www.suruga-ya.com/en/product/186114064',
	'https://www.suruga-ya.com/en/product/186136845'
]

for x in surugayaPages:
	time.sleep(3.0)
	content = requests.get(x).text
	#print(content)

	soup = BeautifulSoup(content, "lxml")
	addToCartBtn = soup.find("button",id='add-cart-btn')
	if addToCartBtn is not None:
		price = soup.find("input", class_="priceValue")
		JPY = int(price["value"])
		priceVal = f"¥{JPY:,.2f}"
		priceVal = priceVal.rstrip("0").rstrip(".")


	print(addToCartBtn)


	if addToCartBtn is not None:
		print("PRODUCT AVAILABLE")
		print(priceVal)
	else:
		print("PRODUCT UNAVAILABLE")




app = Flask(__name__)

@app.route("/")
def hello():
	return "Hello world!"



#look for id "add-cart-btn"
#general loop of the program

#START
#	allow entries of pages into site (check for formatting, must be of supported site types, perform different checks based on base site entry)

#need to find a way to allow entry of pages and sites, possibly through a web server that is hosted when the bot runs, dont know yet.