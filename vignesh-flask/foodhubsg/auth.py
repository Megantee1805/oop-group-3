import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

from foodhubsg.db import get_db, query_db, init_db


bp = Blueprint('auth', __name__, url_prefix='/auth')


def login_required(view):
    """View decorator that redirects anonymous users to the login page."""
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))

        return view(**kwargs)

    return wrapped_view


@bp.before_app_request
def load_logged_in_user():
    """If a user id is stored in the session, load the user object from
    the database into ``g.user``."""
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        g.user = get_db().execute(
            'SELECT * FROM user WHERE id = ?', (user_id,)
        ).fetchone()


@bp.route('/register', methods=('GET', 'POST'))
def register():
    session.clear()
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        name = request.form['name']
        height = request.form['height']
        weight = request.form['weight']
        db = get_db()
        check_user = db.execute('SELECT id FROM user WHERE email = ?', (email,)).fetchone()
        error = None

        if not email:
            error = 'Please enter your email'
        elif not password:
            error = 'Please enter your password'
        elif not name:
            error = 'Please enter your name'
        elif not weight:
            error = 'Please enter your weight'
        elif not height:
            error = 'Please enter your height'
        elif check_user is not None:
            error = 'This email ({}) is already registered.'.format(email)

        if error is None:
            db.execute(
                'INSERT INTO user (email, password, name, height, weight) VALUES (?, ?, ?, ?, ?)',
                (email, generate_password_hash(password), name, height, weight)
            )
            db.commit()

            return redirect(url_for('auth.login'))

        flash(error)

    return render_template('auth/register.html')


@bp.route('/login', methods=('GET', 'POST'))
def login():
    """Log in a registered user by adding the user id to the session."""
    session.clear()
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        db = get_db()
        error = None
        user = db.execute(
            'SELECT * FROM user WHERE email = ?', (email,)
        ).fetchone()

        if user is None:
            error = 'Incorrect email entered'
        elif not check_password_hash(user['password'], password):
            error = 'Incorrect password entered'

        if error is None:
            # store the user id in a new session and return to the index
            session.clear()
            session['user_id'] = user['id']
            return redirect(url_for('index'))

        flash(error)

    return render_template('auth/login.html')

@login_required
@bp.route('/settings', methods=['POST', 'GET'])
def settings():
        init_db()
        db = get_db()
        email = query_db('SELECT * FROM user Where email = ?', args=([g.email]), One=True)
        name = query_db('SELECT * FROM user Where name = ?', args =([g.name]), One=True)
        password = query_db('SELECT * FROM user WHERE password = ?', args = ([g.password]), One=True)
        height = query_db('SELECT * FROM user WHERE height = ?', args =([g.height]), One=True)
        weight = db.execute('SELECT * FROM user WHERE weight = ?', args =([g.weight]), One=True)
        return render_template("auth/settings.html", email=email, name=name, password=password,
                               height=height, weight=weight)


@bp.route('/logout')
def logout():
    """Clear the current session, including the stored user id."""
    session.clear()
    return redirect(url_for('auth.login'))
