from time import sleep
from apscheduler.schedulers.background import BackgroundScheduler,BlockingScheduler

import scraper.config as _G

def scrapeScheduler(func):
    scheduler = BlockingScheduler()

    scheduler.add_job(func,'cron',hour=_G.hourSchedule, minute=_G.minuteSchedule)

    scheduler.start()