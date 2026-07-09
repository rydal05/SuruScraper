import logging
from pathlib import Path
import sys

sys.path.append("..")

from tests.test_logger import configure_logging
from tests.test_autodb import TEST

ROOT_PATH = Path(__file__).resolve().parent.parent
database_folder = ROOT_PATH/"data"/"tests"/"test_dbs/"

def main():
    print("HELLO")
    configure_logging()
    logger = logging.getLogger(__name__)
    logger.info('-=Logger Configured=-')

    logger.info('Clearing old databases')
    for file in database_folder.iterdir():
        if file.is_file():
            file.unlink()

    logger.info('Running autoseed and autodb')
    TEST()


main()