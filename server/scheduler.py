import logging
logger = logging.getLogger(__name__)
logger.info(f'Started in {__name__}')

from time import sleep
from apscheduler.schedulers.background import BackgroundScheduler
import configparser
import os



config = configparser.ConfigParser()

config.read('config.ini')

c_hour = config['settings']['hourSchedule']
c_minute = config['settings']['minuteSchedule']

def scrapeScheduler(func):
    scheduler = BackgroundScheduler()

    scheduler.add_job(func,'cron',hour=c_hour, minute=c_minute)

    scheduler.start()