import sqlite3
from datetime import datetime

import click
from flask import current_app, g

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

def init_db():
    db = get_db()

    with current_app.open_resource('schema.sql') as f:
        db.executescript(f.read().decode('utf8'))

@click.command('init-db')
def init_db_command():
    """Clear the existing data and create new tables."""
    init_db()
    click.echo('Initialized the database.')

def has_users():
    try:
        return get_db().execute('SELECT 1 FROM user LIMIT 1').fetchone() is not None
    except sqlite3.OperationalError:
        return False

def get_all_items():
    try:
        return get_db().execute(
            'SELECT id, url, name, price, lastSeenDate, lastSeenTime, cleaned '
            'FROM wishlist ORDER BY id DESC'
        ).fetchall()
    except sqlite3.OperationalError:
        return []

def get_item_by_id(item_id: int):
    try:
        return get_db().execute(
            'SELECT id, url, name, price, lastSeenDate, lastSeenTime, cleaned '
            'FROM wishlist WHERE id = ?',
            (item_id,),
        ).fetchone()
    except sqlite3.OperationalError:
        return None

def insert_wishlist(link: str):
    db = get_db()
    db.execute(
        'INSERT OR IGNORE INTO wishlist (url, name, price, lastSeenDate, lastSeenTime, cleaned) '
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
        'INSERT OR IGNORE INTO wishlist (url, name, price, lastSeenDate, lastSeenTime, cleaned) '
        'VALUES (?, ?, 0, NULL, NULL, 0)',
        (url, name),
    )
    db.commit()

def update_item(item_id: int, name=None, price=None, last_seen_date=None, last_seen_time=None, cleaned=None):
    fields = []
    values = []

    if name is not None:
        fields.append('name = ?')
        values.append(name)
    if price is not None:
        fields.append('price = ?')
        values.append(price)
    if last_seen_date is not None:
        fields.append('lastSeenDate = ?')
        values.append(last_seen_date)
    if last_seen_time is not None:
        fields.append('lastSeenTime = ?')
        values.append(last_seen_time)
    if cleaned is not None:
        fields.append('cleaned = ?')
        values.append(1 if cleaned else 0)

    if not fields:
        return

    values.append(item_id)
    db = get_db()
    db.execute(
        f'UPDATE wishlist SET {", ".join(fields)} WHERE id = ?',
        values,
    )
    db.commit()

def delete_item(item_id: int):
    db = get_db()
    db.execute('DELETE FROM wishlist WHERE id = ?', (item_id,))
    db.commit()

def set_item_status(item_id, in_stock, price, last_checked_at):
    if last_checked_at is None:
        update_item(item_id, cleaned=not in_stock, price=price)
        return

    update_item(
        item_id,
        cleaned=not in_stock,
        price=price,
        last_seen_date=last_checked_at.date().isoformat(),
        last_seen_time=last_checked_at.strftime('%H:%M'),
    )

sqlite3.register_converter(
    'timestamp', lambda v: datetime.fromisoformat(v.decode())
)

def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)


def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row

    return g.db

def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()

def init_db():
    db = get_db()

    with current_app.open_resource('schema.sql') as f:
        db.executescript(f.read().decode('utf8'))

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
