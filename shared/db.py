import sqlite3
from datetime import datetime

import click
from flask import current_app, g

from pathlib import Path 

# specific to the things I want, older titles have these prefixes that I want
# to remove for better readability
prefixes = [
    "Doujin GAME CD Software",
    "General dojinshi for men Other games",
    "General dojinshi for men",
    "Other Games",
    "Dojin music CD-software"
] #TODO: Ideally want some way to add on to this in the future when the webapp is up and running.

BASE_DIR = Path(__file__).resolve().parent
db_path = BASE_DIR.parent/"data"/"database.db"
seed_path = BASE_DIR.parent/"data"/"seed.txt"

def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )

        g.db.row_factory = sqlite3.Row
    
    return g.db

def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()

def get_prefixes():
    return prefixes

def seed_db():
    surugayaPages = []

    if Path(db_path).exists(): # return when we already have a db initialized
        print("database exists")
        return
    if not Path(seed_path).exists(): # return if a database seed doesn't exist (seed files consist of line-break delimited item pages)
        print("seed doesn't exist") 
        return

    with open(seed_path,'r') as file:
        for line in file:
            line = line.strip("\n") # always remove \n from the file this just makes it easier for formatting on my end
            surugayaPages.append((line,))
            print(line)

    with sqlite3.connect(db_path) as conn:
        cur = conn.cursor()

        # table that contains item data pertinent to all wishlisted items
        cur.execute("""
            CREATE TABLE IF NOT EXISTS wishlist (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                    url TEXT UNIQUE,
                    name TEXT,
                    price INTEGER,
                    lastSeenDate TEXT,
                    lastSeenTime TEXT
            )
        """)

        cur.execute("SELECT COUNT(*) FROM wishlist")
        if cur.fetchone()[0] == 0:
            print("Empty database detected. Seeding...")
            cur.executemany(
                "INSERT OR IGNORE INTO wishlist (url, name, price) VALUES (?,'BLANK',0)", surugayaPages 
                #TODO: add # of times sucessfully iterated over while in stock, general idea is that items have a maximum of 3 times you will be reminded that they're in stock before it stops sending out "IN STOCK" notifications  
                #(still updates page/database information obviously)
            )
            conn.commit()

            
def insert_wishlist(link: str):
    with sqlite3.connect(db_path) as conn:
        cur = conn.cursor()

        cur.execute(
            "INSERT or IGNORE INTO wishlist (link, name, price) VALUES (?,'BLANK', 0)"
        )


    return True

def pop_wishlist():
    return

def get_all_items():
    return

def get_item_by_id(id: int):
    return

def add_item(url, name):
    return

def update_item():
    return

def delete_item(id: int):
    return

def set_item_status(id, in_stock, price,last_checked_at):
    return