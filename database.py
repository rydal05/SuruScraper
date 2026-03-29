import sqlite3

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

prefixes = ["Doujin GAME CD Software", "General dojinshi for men Other games"]

def get_prefixes():
    return prefixes

def seed_db():
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

            
def insert_wishlist(link: str):
    return

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

