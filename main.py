import scrape
import database

if __name__ == "__main__":
    database.seed_db()
    
    scrape.suru_scrape_task()
