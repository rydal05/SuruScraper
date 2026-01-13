This project is purely a fun tool I decided to create for myself as a result of a overseas shopping website I use lacking any real notifier function for its wishlisting feature. All of this culumnating in an effort ultimately supporting my collection of fanworks pertaining to one of my favorite indie video games ever created.

Resources used:
- Python
- [BeautifulSoup4](https://www.crummy.com/software/BeautifulSoup/bs4/doc/#quick-start)
- [smtplib](https://docs.python.org/3/library/smtplib.html) 
- [SQLite](https://docs.python.org/3.13/library/sqlite3.html#tutorial)
- [Flask](https://flask.palletsprojects.com/en/stable/tutorial/factory/)
- [Docker](https://docs.docker.com/guides/python/containerize/)

SuruScraper is a SAAS CRUD (Create, Read, Update, Delete) web app hosted locally on my own network by my Homelab, accessible via web browser for configuring and gathering updates in real time. This allows me to pop and insert items into the wishlist checking queue from any device whenever necessary. At a very basic level, it will cache information of all pages submitted to its database, and periodically check if they have gone into stock within the determined interval. Additionally performing search functions to see if any new items I have not yet discovered have entered the catalogue of the site. As a result of the property I'm going after being so old, additionally being Japanese items sold at the COMIKET conventions over a decade ago, there are certainly going to be some items that have flown under my radar. So some functionality to submit search terms to be looked over also exists. Finally, the application (upon detecting something desired returning to stock) will shoot out an email to my personal address notifying me the moment it locates an in-stock item.
