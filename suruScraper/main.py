import suruScraper.scrape as scrape
import suruScraper.database as database
import suruScraper.scheduler as scheduler

if __name__ == "__main__":
    print("Database precursor")
    database.seed_db() # seeds links to scrape from
    print("Scrape precursor")
    scrape.suru_scrape_task() # initial pass in order to update DB for links passed
    # "game loop"
    scheduler.scrapeScheduler(scrape.suru_scrape_task) # scheduled scrape that 

    print("Hello")
