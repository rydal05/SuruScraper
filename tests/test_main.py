import logging
from pathlib import Path
import sys

sys.path.append("..")

from tests.test_logger import configure_logging
from tests.test_autodb import TEST

def main():
    print("HELLO")
    configure_logging()
    logger = logging.getLogger(__name__)
    logger.info('-=Logger Configured=-')


    logger.info('Running autoseed and autodb')
    TEST()


main()