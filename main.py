import scrape
import database

if __name__ == "__main__":
    print("Database precursor")
    database.seed_db() # seeds links to scrape from
    print("Scrape precursor")
    scrape.suru_scrape_task() # initial pass in order to update DB for links passed

    # "game loop"
