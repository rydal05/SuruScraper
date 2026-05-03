import scrape
import database
import scheduler

if __name__ == "__main__":
    print("Database precursor")
    database.seed_db() # seeds links to scrape from
    print("Scrape precursor")
    scrape.suru_scrape_task() # initial pass in order to update DB for links passed
    # "game loop"
    scheduler.scrapeScheduler(scrape.suru_scrape_task) # scheduled scrape that runs on the hour XX:00
