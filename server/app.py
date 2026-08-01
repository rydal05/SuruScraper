import logging

try:
    from . import create_app
except ImportError:
    from server import create_app

import threading
import asyncio

from server.scheduler import scrapeScheduler
from server.scrape import suru_scrape_task
from server.logger import configure_logging

app = create_app()

if __name__ == '__main__':
    print('running main')
    configure_logging()
    logger = logging.getLogger(__name__)
    logger.info('-=Logger Configured=-')

    with app.app_context():
        logger.info('Scheduled scrape task')
        scrapeScheduler(suru_scrape_task())
    logger.info('App running')
    app.run(debug=True)