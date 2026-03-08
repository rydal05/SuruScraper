from apscheduler.schedulers.background import BackgroundScheduler

from dotenv import load_dotenv
from scrape import suru_scrape_task


load_dotenv()
scheduler = BackgroundScheduler()

def schedule_scrape():
    scheduler.add_job(func=suru_scrape_task,trigger="interval",hours=1)
    scheduler.start()