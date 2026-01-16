import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

from suru.db import get_db

bp = Blueprint('auth', __name__, url_prefix='/auth')


@bp.route('/wishlist', methods=('GET','POST'))
def register():
    if request.method == 'POST':




    return render_template('wishlist.html')