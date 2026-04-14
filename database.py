import sqlite3
from pathlib import Path

# specific to the things I want, older titles have these prefixes that I want
# to remove for better readability
prefixes = ["Doujin GAME CD Software", "General dojinshi for men Other games"]

def get_prefixes():
    return prefixes

def seed_db():
    surugayaPages = []

    if Path("suru.db").exists(): # return when we already have a db initialized
        print("database exists")
        return
    if not Path("seed.txt").exists(): # return if a database seed doesn't exist
        print("seed doesn't exist")
        return

    with open('seed.txt','r') as file:
        for line in file:
            line = line.strip("\n") # always remove \n from the file this just makes it easier for formatting on my end
            surugayaPages.append((line,))
            print(line)

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
                "INSERT OR IGNORE INTO wishlist (url, name, price) VALUES (?,'BLANK',0)", surugayaPages
            )
            conn.commit()

            
def insert_wishlist(link: str):
    with sqlite3.connect('suru.db') as conn:
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

