from pathlib import Path
import sqlite3

import test_logger as TL

ROOT_PATH = Path(__file__).resolve().parent.parent
seed_folder = ROOT_PATH/"suruscrapr"/"tests"/"test_seeds"
database_folder = ROOT_PATH/"suruscrapr"/"tests"/"test_dbs"
schema_file = ROOT_PATH/"schema.sql"

def TEST():
    init_dbs()

    seed_dbs()

def seed_dbs():
    for index, seed in enumerate(seed_folder.iterdir()):
        # with open(database_folder/f"test_database{i}.db","w") as file:
        #     pass

        db_path = database_folder/f"test_database{index}"

        with sqlite3.connect(db_path) as con_db:
            cur_db = con_db.cursor()

        pages = []

        
        with open(seed, 'r') as file:
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

def init_dbs():
    for index in enumerate(seed_folder.iterdir()):
        db_path = database_folder/f"test_database{index}.db"

        with sqlite3.connect(db_path) as con_db:
            cur_db = con_db.cursor()

            with open(schema_file, 'r') as f:
                schema_sql = f.read().strip()

            try:
                for statement in schema_sql.split(';'):
                    stripped_statement = statement.strip()
                    if stripped_statement:
                        cur_db.execute(stripped_statement)

                con_db.commit()
            except sqlite3.Error as e:
                TL.logging.error(f'Error occurred: {e}')
                con_db.rollback()