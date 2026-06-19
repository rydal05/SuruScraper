from time import sleep
from apscheduler.schedulers.background import BackgroundScheduler,BlockingScheduler



def scrapeScheduler(func):
    scheduler = BlockingScheduler()

    scheduler.add_job(func,'cron',hour=config.hourSchedule, minute=config.minuteSchedule)

    scheduler.start()