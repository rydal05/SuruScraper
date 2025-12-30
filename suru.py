from bs4 import BeautifulSoup
import requests

with open('IN_STOCK.html','r') as html_file:
    content = html_file.read()
    #print(content)

    soup = BeautifulSoup(content, "lxml")
    addToCartBtn = soup.find_all("button",id='add-cart-btn')
    priceLabel = soup.find("input", class_="priceValue")

    print(addToCartBtn)
    if len(addToCartBtn) != 0:
        print("PRODUCT AVAILABLE")
        price = priceLabel.value.Text
        print(price)
    elif len(addToCartBtn) > 1:
        print("POTENTIAL SITE CHANGE: Multiple add to cart buttons appear")
    else:
        print("PRODUCT UNAVAILABLE")




#look for id "add-cart-btn"
#general loop of the program

#START
#	check file links and cache current state of pages
#	perform checks on whether item is in stock or out of stock
#	report (through some messaging medium undecided)
#	repeat on timed interval 
#	allow entries of pages into site (check for formatting, must be of supported site types, perform different checks based on base site entry)

#need to find a way to allow entry of pages and sites, possibly through a web server that is hosted when the bot runs, dont know yet.