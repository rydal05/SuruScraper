import sqlite3

from flask import Blueprint, flash, g, redirect, render_template, request, session, url_for

from suruscrapr.auth import login_required
from suruscrapr.db import get_all_items, get_db

bp = Blueprint('wishlist', __name__)

DEFAULT_SETTINGS = {
    'notification': 'web',
    'scan_interval': 'hourly',
    'scan_time': 'XX:00',
    'theme': 'light',
}


@bp.route('/')
def index():
    if g.user is None:
        return redirect(url_for('auth.login' if g.account_exists else 'auth.register'))

    items = get_all_items()
    settings = {**DEFAULT_SETTINGS, **session.get('dashboard_settings', {})}
    return render_template('wishlist/index.html', items=items, settings=settings)


@bp.route('/create', methods=('GET', 'POST'))
@login_required
def create():
    if request.method == 'POST':
        url = request.form['url'].strip()
        display_name = request.form['name'].strip() or 'BLANK'

        if not url:
            flash('A wishlist URL is required.')
        else:
            try:
                db = get_db()
                db.execute(
                    'INSERT OR IGNORE INTO wishlist (url, name, price, lastSeenDateTime, cleaned) '
                    'VALUES (?, ?, 0, NULL, NULL, 0)',
                    (url, display_name),
                )
                db.commit()
            except sqlite3.OperationalError:
                flash('Initialize the database first with `flask --app suruscrapr init-db`.')
            else:
                flash('Wishlist item added.')
                return redirect(url_for('wishlist.index'))

    return render_template('wishlist/create.html')


@bp.route('/scrape-now', methods=('POST',))
@login_required
def scrape_now():
    try:
        from suruscrapr.scrape import suru_scrape_task

        suru_scrape_task()
    except sqlite3.OperationalError:
        flash('Initialize the database first with `flask --app suruscrapr init-db`.')
    except Exception as exc:
        flash(f'Scrape failed: {exc}')
    else:
        flash('Scrape started and completed for the current wishlist.')

    return redirect(url_for('wishlist.index'))


@bp.route('/settings', methods=('GET', 'POST'))
@login_required
def settings():
    if request.method == 'POST':
        action = request.form.get('action', 'save')

        if action == 'import_seed':
            try:
                from db import seed_db

                seed_db()
            except sqlite3.OperationalError:
                flash('Initialize the database first with `flask --app suruscrapr init-db`.')
            else:
                flash('Seed links imported from data/seed.txt.')
            return redirect(url_for('wishlist.settings'))

        session['dashboard_settings'] = {
            'notification': request.form.get('notification', DEFAULT_SETTINGS['notification']),
            'scan_interval': request.form.get('scan_interval', DEFAULT_SETTINGS['scan_interval']),
            'scan_time': request.form.get('scan_time', DEFAULT_SETTINGS['scan_time']),
            'theme': request.form.get('theme', DEFAULT_SETTINGS['theme']),
        }
        flash('Settings saved for this session.')
        return redirect(url_for('wishlist.settings'))

    settings = {**DEFAULT_SETTINGS, **session.get('dashboard_settings', {})}
    return render_template('wishlist/settings.html', settings=settings)


@bp.route('/<int:item_id>/delete', methods=('POST',))
@login_required
def delete(item_id):
    db = get_db()
    db.execute('DELETE FROM wishlist WHERE id = ?', (item_id,))
    db.commit()
    flash('Wishlist item removed.')
    return redirect(url_for('wishlist.index'))