import scraper.scrape as scrape
import shared.db as db
import scraper.scheduler as scheduler

def scheduledScrape():
    print("Database precursor")
    db.seed_db() # seeds links to scrape from (utilizes a .txt file with links already \n delimited but might switch over to auth login on website and grabbing wishlists to do so)
    print("Scrape precursor")
    scrape.suru_scrape_task() # initial pass in order to update DB for links passed
    # "game loop"
    scheduler.scrapeScheduler(scrape.suru_scrape_task) # scheduled scrape that runs every hour on XX:00