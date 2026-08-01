import logging
logger = logging.getLogger(__name__)
logger.info(f'Started in {__name__}')

from pathlib import Path
from flask import Flask

import threading
import asyncio

from server.scheduler import scrapeScheduler
from server.scrape import suru_scrape_task

def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)

    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=str(Path(__file__).resolve().parent.parent / 'data' / 'database.db'),
    )

    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)

    Path(app.instance_path).mkdir(parents=True, exist_ok=True)

    from . import auth, db, wishlist

    db.init_app(app)
    app.register_blueprint(auth.bp)
    app.register_blueprint(wishlist.bp)

    return app