import time
from bs4 import BeautifulSoup
import requests
import sqlite3
from apscheduler.schedulers.background import BackgroundScheduler
from smtplib import SMTP
import os
from dotenv import load_dotenv

load_dotenv()
scheduler = BackgroundScheduler()

surugayaPages = [
	('https://www.suruga-ya.com/en/product/ZHORE50831', 'BLANK', 0),
	('https://www.suruga-ya.com/en/product/ZHORE138875', 'BLANK', 0),
	('https://www.suruga-ya.com/en/product/ZHORE70652', 'BLANK', 0),
	('https://www.suruga-ya.com/en/product/ZHORE29719', 'BLANK', 0),
	('https://www.suruga-ya.com/en/product/ZHORE79987', 'BLANK', 0),
	('https://www.suruga-ya.com/en/product/ZHORE79987', 'BLANK', 0),
	('https://www.suruga-ya.com/en/product/ZHORE80042', 'BLANK', 0),
	('https://www.suruga-ya.com/en/product/ZHORE229720', 'BLANK', 0),
	('https://www.suruga-ya.com/en/product/ZHORE138862', 'BLANK', 0),
	('https://www.suruga-ya.com/en/product/ZHORE55361', 'BLANK', 0),
	('https://www.suruga-ya.com/en/product/ZHORE9659', 'BLANK', 0),
	('https://www.suruga-ya.com/en/product/186011708', 'BLANK', 0),
	('https://www.suruga-ya.com/en/product/186023385', 'BLANK', 0),
	('https://www.suruga-ya.com/en/product/186023384', 'BLANK', 0),
	('https://www.suruga-ya.com/en/product/186147823', 'BLANK', 0),
	('https://www.suruga-ya.com/en/product/186118307', 'BLANK', 0),
	('https://www.suruga-ya.com/en/product/186114064', 'BLANK', 0),
	('https://www.suruga-ya.com/en/product/186136845', 'BLANK', 0)
]

personal_email = os.getenv("EMAIL")


subject = f"Suruga-ya Product in Stock! [Product info maybe]"
message = f"An item on your wishlist in in stock: [product name hyperlinked] @ [product price]. "

prefixes = ["Doujin GAME CD Software", "General dojinshi for men Other games"]



def suru_scrape_task():
    #context manager
    with sqlite3.connect('suru.db') as conn:
        cursor = conn.cursor()
        #grab id
        items = cursor.execute("SELECT id, url, name FROM wishlist").fetchall()

        for item_id, url, original_name in items:
            try:
                response = requests.get(url, timeout=10)
                if response.status_code != 200: continue
                soup = BeautifulSoup(response.content, "lxml")
                
                # Update outdated names
                name = original_name

                if original_name == "BLANK":
                    title_tag = soup.find("h1", class_="title_product")
                    if title_tag:
                        name = title_tag.text.strip()
                    for prefix in prefixes:
                        name = name.removeprefix(prefix).strip()
                    cursor.execute("UPDATE wishlist SET name = ? WHERE id = ?", (name,))
                # Check if available
                addToCartBtn = soup.find("button",id='add-cart-btn')

                if addToCartBtn:
                    price_input = soup.find("input", class_="priceValue")
                    price_val = price_input["value"] if price_input else "Unknown"
                    print(f"{name}: AVAILABLE @ ¥{price_val}")
                else:
                    print(name + ": PRODUCT UNAVAILABLE")

                conn.commit()
                time.sleep(10.0)
            except Exception as e:
                print(f"Error scraping {url}:{e}")

def init():
    with sqlite3.connect('suru.db') as conn:
        cur = conn.cursor()

        cur.execute("""
            CREATE TABLE IF NOT EXISTS wishlist (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                    url TEXT UNIQUE,
                    name TEXT,
                    price INTEGER        
            )
        """)

        cur.execute("SELECT COUNT(*) FROM wishlist")
        if cur.fetchone()[0] == 0:
            print("Empty database detected. Seeding...")
            cur.executemany(
                "INSERT OR IGNORE INTO wishlist (url, name, price) VALUES (?,?,?)", surugayaPages
            )
            conn.commit()
    
    scheduler.add_job(func=suru_scrape_task,trigger="interval",hours=1)
    scheduler.start()