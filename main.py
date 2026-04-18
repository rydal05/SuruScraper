import scrape
import database

if __name__ == "__main__":
    print("Database precursor")
    database.seed_db()
    print("Scrape precursor")
    scrape.suru_scrape_task()
