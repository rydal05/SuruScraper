import logging
from pathlib import Path
import sqlite3

import tests.test_logger as TL

ROOT_PATH = Path(__file__).resolve().parent.parent
seed_folder = ROOT_PATH/"data"/"tests"/"test_seeds/"
database_folder = ROOT_PATH/"data"/"tests"/"test_dbs/"
schema_file = ROOT_PATH/"server"/"schema.sql"

def TEST():
    TL.configure_logging()
    TL.logger = logging.getLogger(__name__)
    TL.logger.info('-=Logger Configured=-')
    TL.logging.info("Hello we called this from TL")
    init_dbs()

def seed_db(index: int):
    db_path = database_folder/f"test_database{index}.db"

    with sqlite3.connect(db_path) as con_db:
        cur_db = con_db.cursor()
        pages = []

        with open(seed_folder/f"testseed{index}.txt", 'r') as file:
            for line in file:
                cleaned_line = line.strip("\n")
                pages.append((cleaned_line,))
                TL.logging.info(f"Found: {cleaned_line}")
        try:
            cur_db.executemany("INSERT OR IGNORE INTO wishlist (url) VALUES (?)", pages)
            con_db.commit()
        except sqlite3.Error as e:
            TL.logging.error(f'Error occurred while seeding: {e}')
            con_db.rollback()
            TL.logging.error

def init_dbs():
    for index, path in enumerate(seed_folder.iterdir()):
        db_path = database_folder/f"test_database{index}.db"
        
        print(db_path)

        with sqlite3.connect(db_path) as con_db:
            con_db.row_factory = sqlite3.Row
            
            cur_db = con_db.cursor()

            with open(schema_file, 'r') as f:
                schema_sql = f.read().strip()

            try:
                for statement in schema_sql.split(';'):
                    stripped_statement = statement.strip()
                    if stripped_statement:
                        cur_db.execute(stripped_statement)
                
                seed_db(index)
                con_db.commit()
            except sqlite3.Error as e:
                TL.logging.error(f'Error occurred: {e}')
                con_db.rollback()