# SuruScraper

SuruScraper is a wishlist & databasing service for customers of Suruga-ya and Suruga-ya.jp. It allows for autonomous monitoring and reporting of stock status for items on the Suruga-ya platform. Some features of this software include: last time spotted in stock, last reported price, instantaneous notifications for PC and mobile, and more. 

## Features
* Autonomous item scraping from suruga-ya and suruga-ya.jp
* Persistent private database 
* Web accessible
* Browser push notifications
* Customizable intervals


## How to Setup

1. Build the Docker container using the pre-configured docker-compose.yml
2. Initialize the database with `flask --app suruscrapr init-db`
3. Launch the app with [COMMAND]

## Tools
* Python 3.14
* BeautifulSoup4
* SQLite
* Flask
* Docker