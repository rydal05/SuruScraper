import time
from bs4 import BeautifulSoup
import requests
import sqlite3

from database_handler import get_prefixes



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
                    for prefix in get_prefixes():
                        name = name.removeprefix(prefix).strip()
                    cursor.execute("UPDATE wishlist SET name = ? WHERE id = ?", (name, item_id))
                # Check if available
                addToCartBtn = soup.find("button",id='add-cart-btn')

                if addToCartBtn:
                    price_input = soup.find("input", class_="priceValue")
                    price_val = price_input["value"] if price_input else "Unknown"
                    print(f"{name}: AVAILABLE @ ¥{price_val}")
                else:
                    print(name + ": PRODUCT UNAVAILABLE")

                conn.commit()
                time.sleep(3.0)
            except Exception as e:
                print(f"Error scraping {url}:{e}")