from scrape import suru_scrape_task
from database_handler import seed_db

if __name__ == "__main__":
    seed_db()
    
    suru_scrape_task()
