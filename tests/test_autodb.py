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
    for i, seed in enumerate(seed_folder.iterdir()):
        with open(database_folder/f"test_database{i}.db","w") as file:
            pass

        db = database_folder/f"test_database{i}"

        con_db = sqlite3.connect(db)
        cur_db = con_db.cursor()
        pages = []

        if not Path(seed).exists():
            TL.logging.error("seed DNE")
            return
        
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
        finally:
            cur_db.close()
            con_db.close()

def init_dbs():
    for i in enumerate(seed_folder.iterdir()):
        with open(database_folder/f"test_database{i}.db","w") as file:
            pass
        
        db = database_folder/f"test_database{i}.db"

        con_db = sqlite3.connect(db)
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

        finally:
            cur_db.close()
            con_db.close()
            