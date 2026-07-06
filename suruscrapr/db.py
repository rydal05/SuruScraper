import sqlite3
from datetime import datetime

import click
from flask import current_app, g

from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
seed_path = BASE_DIR.parent/"data"/"seed.txt"
schema_file = BASE_DIR/"schema.sql"

def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES,
        )
        g.db.row_factory = sqlite3.Row

    return g.db


def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()


def has_users():
    try:
        return get_db().execute('SELECT 1 FROM user LIMIT 1').fetchone() is not None
    except sqlite3.OperationalError:
        return False


def get_all_items():
    try:
        return get_db().execute(
            'SELECT id, url, name, price, dateLastSeen, timeLastSeen, cleaned '
            'FROM wishlist ORDER BY id DESC'
        ).fetchall()
    except sqlite3.OperationalError:
        return []


def get_item_by_id(item_id: int):
    try:
        return dict(get_db().execute(
            'SELECT id, url, name, price, dateLastSeen, timeLastSeen, cleaned '
            'FROM wishlist WHERE id = ?',
            (item_id,)
        ).fetchone())
    except sqlite3.OperationalError:
        return None


def insert_wishlist(link: str):
    db = get_db()
    db.execute(
        'INSERT OR IGNORE INTO wishlist (url, name, price, dateLastSeen, timeLastSeen, cleaned) '
        "VALUES (?, 'BLANK', 0, NULL, NULL, 0)",
        (link,),
    )
    db.commit()
    return True


def pop_wishlist():
    return None


def add_item(url, name):
    db = get_db()
    db.execute(
        'INSERT OR IGNORE INTO wishlist (url, name, price, dateLastSeen, timeLastSeen, cleaned) '
        'VALUES (?, ?, 0, NULL, NULL, 0)',
        (url, name),
    )
    db.commit()


def update_item(item_id: str, url=None, name=None, price=None, dateLastSeen=None, timeLastSeen=None):
    fields = []
    values = []

    if item_id is not None:
        fields.append('SuruID = ?')
        values.append(item_id)

    if url is not None:
        fields.append('url = ?')
        values.append(url)

    if name is not None:
        fields.append('name = ?')
        values.append(name)

    if price is not None:
        fields.append('price = ?')
        values.append(price)

    if dateLastSeen is not None:
        fields.append('dateLastSeen = ?')
        values.append(dateLastSeen)

    if timeLastSeen is not None:
        fields.append('timeLastSeen = ?')
        values.append(timeLastSeen)

    if not fields:
        return

    values.append(item_id)
    db = get_db()
    db.execute(
        f'UPDATE wishlist SET {", ".join(fields)} WHERE id = ?',
        values,
    )
    db.commit()

def isCleaned(item_id: str):
    dbItem = get_item_by_id(item_id)

    if dbItem:
        return dbItem.get('cleaned')
    return None


def delete_item(item_id: int):
    db = get_db()
    db.execute('DELETE FROM wishlist WHERE id = ?', (item_id,))
    db.commit()

sqlite3.register_converter(
    'timestamp', lambda v: datetime.fromisoformat(v.decode())
)


def init_db():
    db = get_db()
    cursor = db.cursor() 

    with open(schema_file, 'r') as f:
        schema_sql = f.read().strip()

    try:
        for statement in schema_sql.split(';'):
            stripped_statement = statement.strip()
            if stripped_statement:
                cursor.execute(stripped_statement)

        seed_db()
        db.commit()
    except sqlite3.Error as e:
        print(f'Error occurred: {e}')
        # db.rollback()

    finally:
        db.close()

def seed_db():
    db = get_db()
    cursor = db.cursor()
    pages = []

    if not Path(seed_path).exists():
        print("seed DNE")
        return
    
    with open(seed_path, 'r') as file:
        for line in file:
            cleaned_line = line.strip("\n")
            pages.append((cleaned_line,))

    try:
        cursor.executemany("INSERT OR IGNORE INTO wishlist (url) VALUES (?)", pages)
        db.commit()
    except sqlite3.Error as e:
        print(f'Error occurred while seeding: {e}')
        # db.rollback()

@click.command('init-db')
def init_db_command():
    """Clear the existing data and create new tables."""
    init_db()
    click.echo('Initialized the database.')


sqlite3.register_converter(
    "timestamp", lambda v: datetime.fromisoformat(v.decode())
)


def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)