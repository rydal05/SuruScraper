from time import sleep
from apscheduler.schedulers.background import BackgroundScheduler,BlockingScheduler
import configparser
import os

config = configparser.ConfigParser()

config.read('config.ini')

c_hour = config['settings']['hourSchedule']
c_minute = config['settings']['minuteSchedule']


def scrapeScheduler(func):
    scheduler = BlockingScheduler()

    scheduler.add_job(func,'cron',hour=c_hour, minute=c_minute)

    scheduler.start()