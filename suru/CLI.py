import time
from bs4 import BeautifulSoup
import requests
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

# cur.executemany("INSERT INTO wishlist VALUES(?, ?, ?)", surugayaPages) #?'s are used as placeholder/substitutions
# con.commit() #transactions must be committed always after

# for row in cur.execute("SELECT link, name FROM wishlist"): # TODO: do ORDER BY price whenever I get around to having page scrapes obtain that information
# 	print(row)


def suruScrape():
    # runs on an hourly interval, when the clock reaches XX:00
    print("running checks")

    for x in surugayaPages:
        
        content = requests.get(x[0]).text
        #print(content)
        soup = BeautifulSoup(content, "lxml")
        addToCartBtn = soup.find("button",id='add-cart-btn')
        name = soup.find("h1", class_="title_product padL0 text-break").text.strip()

        for prefix in prefixes:
            if name.startswith(prefix):
                name = name.removeprefix(prefix)

        if addToCartBtn is not None:
            price = soup.find("input", class_="priceValue")
            JPY = int(price["value"])
            priceVal = f"¥{JPY:,.2f}"
            priceVal = priceVal.rstrip("0").rstrip(".")     
            print(name + ": PRODUCT AVAILABLE @ " + priceVal)
        else:
            print(name + ": PRODUCT UNAVAILABLE")
        time.sleep(10.0)
    
    print("check finished")

def main():
    print("Scheduler started")

    
    suruScrape()
    

    # con.close() #like C/C++ file closing, close database when done accessing
            
if __name__ == "__main__":
    main()