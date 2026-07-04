import functools
import secrets
import sqlite3

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

from suruscrapr.db import get_db, has_users

bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('/register', methods=('GET', 'POST'))
def register():
    if has_users() and request.method == 'GET':
        return redirect(url_for('auth.login'))

    if request.method == 'POST':
        username = request.form['username'].strip()
        password = request.form['password']
        db = get_db()
        error = None

        if has_users():
            error = 'An account already exists. Log in instead.'
        elif not username:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'

        if error is None:
            try:
                db.execute(
                    'INSERT INTO user (username, password) VALUES (?, ?)',
                    (username, generate_password_hash(password)),
                )
                db.commit()
            except sqlite3.OperationalError:
                error = 'Initialize the database first with `flask --app suruscrapr init-db`.'
            except sqlite3.IntegrityError:
                error = f'User {username} is already registered.'
            else:
                flash('Account created. Log in to continue.')
                return redirect(url_for('auth.login'))

        flash(error)

    return render_template('auth/firstTimeRegister.html')


@bp.route('/login', methods=('GET', 'POST'))
def login():
    if not has_users():
        return redirect(url_for('auth.register'))

    if request.method == 'POST':
        username = request.form['username'].strip()
        password = request.form['password']
        db = get_db()
        error = None
        user = db.execute(
            'SELECT * FROM user WHERE username = ?', (username,)
        ).fetchone()

        if user is None:
            error = 'Incorrect username.'
        elif not check_password_hash(user['password'], password):
            error = 'Incorrect password.'

        if error is None:
            session.clear()
            session['user_id'] = user['id']
            return redirect(url_for('wishlist.index')) #TODO: make wishlist page dynamic with tabs to switch between wishlists (I.E. 1 table with header tabs to click between)

        flash(error)

    return render_template('auth/login.html')


@bp.route('/forgot-password', methods=('GET', 'POST'))
def forgot_password():
    if not has_users():
        return redirect(url_for('auth.register'))

    if request.method == 'POST':
        username = request.form['username'].strip()
        db = get_db()
        user = db.execute(
            'SELECT id FROM user WHERE username = ?', (username,)
        ).fetchone()

        if not username:
            flash('Username is required.')
        elif user is None:
            flash('No account matches that username.')
        else:
            temporary_password = secrets.token_urlsafe(8)
            db.execute(
                'UPDATE user SET password = ? WHERE id = ?',
                (generate_password_hash(temporary_password), user['id']),
            )
            db.commit()
            flash(f'Temporary password generated for {username}: {temporary_password}')
            return redirect(url_for('auth.login'))

    return render_template('auth/forgotPassword.html')


@bp.before_app_request
def load_logged_in_user():
    g.account_exists = has_users()
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        g.user = get_db().execute(
            'SELECT * FROM user WHERE id = ?', (user_id,)
        ).fetchone()


@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('auth.login' if has_users() else 'auth.register'))


def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login' if g.account_exists else 'auth.register'))

        return view(**kwargs)

    return wrapped_view
