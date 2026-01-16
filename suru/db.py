from bs4 import BeautifulSoup
import requests

import sqlite3
from datetime import datetime

import click
from flask import current_app, g

def get_db():
	if 'db' not in g:
		g.db = sqlite3.connect(
			current_app.config['DATABASE'],
			detect_types = sqlite3.PARSE_DECLTYPES
		)
		g.db.row_factory = sqlite3.Row

	return g.db	

def close_db(e=None):
	db = g.pop('db', None)

	if db is not None:
		db.close()

def init_db():
	db = get_db()

	with current_app.open_resource('schema.sql') as f:
		db.executescript(f.read().decode('utf8'))

@click.command('init-db')
def init_db_command():
	init_db()
	click.echo("initialized database")

sqlite3.register_converter(
	"timestamp", lambda v: datetime.fromisoformat(v.decode())
)

def init_app(app):
	app.teardown_appcontext(close_db)
	app.cli.add_command(init_db_command)


# DELIMIT OLD CODE AND NEW CODE (OLD BELOW NEW ABOVE)


# con = sqlite3.connect("suru.db")
# cur = con.cursor()
# cur.execute("CREATE TABLE wishlist(link,name,price)")


# res = cur.execute("SELECT name FROM sqlite_master")
# res.fetchone()

# cur.execute("""
# 	INSERT INTO wishlist VALUES
#             ('https://www.suruga-ya.com/en/product/ZHORE50831', 'Pedoshin', 0),
#             ('https://www.suruga-ya.com/en/product/ZHORE138875', 'エビゾメ 赫螺 Maru', 0)
# """)

# con.commit()
# res = cur.execute("SELECT link FROM wishlist")
# lis = res.fetchone()
# print(lis)

# res = cur.execute("SELECT name FROM wishlist")
# lis = res.fetchall()
# print(lis)

# surugayaPages = [
# 	('https://www.suruga-ya.com/en/product/ZHORE50831', 'BLANK', 0),
# 	('https://www.suruga-ya.com/en/product/ZHORE138875', 'BLANK', 0),
# 	('https://www.suruga-ya.com/en/product/ZHORE70652', 'BLANK', 0),
# 	('https://www.suruga-ya.com/en/product/ZHORE29719', 'BLANK', 0),
# 	('https://www.suruga-ya.com/en/product/ZHORE79987', 'BLANK', 0),
# 	('https://www.suruga-ya.com/en/product/ZHORE79987', 'BLANK', 0),
# 	('https://www.suruga-ya.com/en/product/ZHORE80042', 'BLANK', 0),
# 	('https://www.suruga-ya.com/en/product/ZHORE229720', 'BLANK', 0),
# 	('https://www.suruga-ya.com/en/product/ZHORE138862', 'BLANK', 0),
# 	('https://www.suruga-ya.com/en/product/ZHORE55361', 'BLANK', 0),
# 	('https://www.suruga-ya.com/en/product/ZHORE9659', 'BLANK', 0),
# 	('https://www.suruga-ya.com/en/product/186011708', 'BLANK', 0),
# 	('https://www.suruga-ya.com/en/product/186023385', 'BLANK', 0),
# 	('https://www.suruga-ya.com/en/product/186023384', 'BLANK', 0),
# 	('https://www.suruga-ya.com/en/product/186147823', 'BLANK', 0),
# 	('https://www.suruga-ya.com/en/product/186118307', 'BLANK', 0),
# 	('https://www.suruga-ya.com/en/product/186114064', 'BLANK', 0),
# 	('https://www.suruga-ya.com/en/product/186136845', 'BLANK', 0)
# ]

# cur.executemany("INSERT INTO wishlist VALUES(?, ?, ?)", surugayaPages) #?'s are used as placeholder/substitutions
# con.commit() #transactions must be committed always after

# for row in cur.execute("SELECT link, name FROM wishlist"): # TODO: do ORDER BY price whenever I get around to having page scrapes obtain that information
# 	print(row)


# con.close() #like C/C++ file closing, close database when done accessing

# for x in surugayaPages:
# 	time.sleep(3.0)
# 	content = requests.get(x).text
# 	#print(content)

# 	soup = BeautifulSoup(content, "lxml")
# 	addToCartBtn = soup.find("button",id='add-cart-btn')
# 	if addToCartBtn is not None:
# 		price = soup.find("input", class_="priceValue")
# 		JPY = int(price["value"])
# 		priceVal = f"¥{JPY:,.2f}"
# 		priceVal = priceVal.rstrip("0").rstrip(".")


# 	print(addToCartBtn)


# 	if addToCartBtn is not None:
# 		print("PRODUCT AVAILABLE")
# 		print(priceVal)
# 	else:
# 		print("PRODUCT UNAVAILABLE")




# app = Flask(__name__)

# @app.route("/")
# def hello():
# 	return "Hello world!"



#look for id "add-cart-btn"
#general loop of the program

#START
#	allow entries of pages into site (check for formatting, must be of supported site types, perform different checks based on base site entry)

#need to find a way to allow entry of pages and sites, possibly through a web server that is hosted when the bot runs, dont know yet.