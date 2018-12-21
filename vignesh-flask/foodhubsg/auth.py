import functools
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

from foodhubsg.db import get_db


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

        if not name:
            error = 'Please enter your name'
        elif not all(char.isalpha() or char.isspace() for char in name):
            error = 'Please only enter alphabets for your name'
        elif not len(name) < 16:
            error = 'Please enter a name below 16 characters'
        elif not height:
            error = 'Please enter your height'
        elif not 0.5 < float(height) < 2.5:
            error = 'Please enter a valid height value in meters'
        elif not weight:
            error = 'Please enter your weight'
        elif not 20 < float(weight) < 250:
            error = 'Please enter a valid weight value in kilograms'
        elif not email:
            error = 'Please enter your email'
        elif not password:
            error = 'Please enter your password'
        elif check_user is not None:
            error = 'This email ({}) is already registered.'.format(email)

        name = name.title()
        email = email.lower()

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
        email = request.form['email'].lower()
        password = request.form['password']
        db = get_db()
        error = None

        email = email.lower()

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


@bp.route('/user_settings', methods=('GET', 'POST'))
@login_required
def user_settings():

    db = get_db()
    food_items = db.execute(
        'SELECT f.id, creator_id, food_name, created, calories, food_code, email'
        ' FROM food_entry f JOIN user u ON f.creator_id = u.id'
        ' WHERE f.creator_id = ?'
        ' ORDER BY datetime(created) DESC',
        (g.user['id'],),
    ).fetchall()


    users = db.execute(
        'SELECT id, name, email, password, height, weight'
        ' FROM user'
        ' WHERE id = ?',
        (g.user['id'],),
    ).fetchall()

    for user in users:
        name = user['name']
        weight = user['weight']
        height = user['height']
        email = user['email']
        password = user['password']

    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        error = None

        if not title:
            error = 'Title is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'UPDATE post SET title = ?, body = ? WHERE id = ?',
                (title, body, id)
            )
            db.commit()
            return redirect(url_for('blog.index'))

    return render_template('auth/user_settings.html',
                           name=name, weight=weight, height=height, password=password)

@bp.route('/confirm')
def confirm():
    return render_template('auth/verification_email.html')

@bp.route('/logout')
def logout():
    """Clear the current session, including the stored user id."""
    session.clear()
    return redirect(url_for('auth.login'))
