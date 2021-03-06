from flask import (Blueprint, flash, redirect, render_template, request, session, url_for, g)
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime
import functools

from foodhubsg.db import get_db


bp = Blueprint('auth', __name__,)


def login_required(view):
    """View decorator that redirects anonymous users to the login page."""
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))
        if g.user["id"] == 0:
            return redirect(url_for('support.support'))
        return view(**kwargs)
    return wrapped_view


def permission_required(view):
    """View decorator that redirects anonymous users to the login page."""
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))
        if g.user["id"] != 0:
            flash("You do not have sufficient privileges to enter that page")
            return redirect(url_for('food.index'))
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
    if g.user is not None:
        return redirect(url_for('food.index'))

    if request.method == 'POST':
        email = request.form['email'].lower()
        password = request.form['password']
        name = request.form['name'].title()
        height = request.form['height']
        weight = request.form['weight']
        location = "Ang Mo Kio"

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
        elif " " in password:
            error = "Please don't enter whitespaces in your password"
        elif check_user is not None:
            error = 'This email ({}) is already registered.'.format(email)

        if error is None:
            db.execute(
                'INSERT INTO user (email, password, name, height, weight, location, status) VALUES (?, ?, ?, ?, ?, ?,?)',
                (email, generate_password_hash(password), name, height, weight, location, 0)
            )
            db.commit()

            success = "Your account ({}) has been successfully registered!".format(email)
            flash(success, "success")

            return redirect(url_for('auth.login'))

        else:
            flash(error)

    return render_template('auth/register.html', datetime=datetime)


@bp.route('/login', methods=('GET', 'POST'))
def login():
    """Log in a registered user by adding the user id to the session."""
    if g.user is not None:
        return redirect(url_for('food.index'))

    if request.method == 'POST':
        error = None
        db = get_db()
        email = request.form['email'].lower()
        password = request.form['password']

        user = db.execute('SELECT * FROM user WHERE email = ?', (email,)).fetchone()

        if user is None:
            error = 'Incorrect email entered'
        elif not check_password_hash(user['password'], password):
                error = 'Incorrect password entered'

        if error is None:
            # store the user id in a new session and return to the index
            session.clear()
            session['user_id'] = user['id']
            if session['user_id'] == 0:
                return redirect(url_for('support.support'))

            return redirect(url_for('index'))

        else:
            flash(error)

    return render_template('auth/login.html', datetime=datetime)


@bp.route('/change_password', methods=('GET', 'POST'))
def change_password():
    if g.user is not None:
        return redirect(url_for('food.index'))

    session.clear()

    if request.method == 'POST':
        email = request.form['email'].lower()
        password = request.form['password']
        db = get_db()
        error = None
        print(password)

        email = email.lower()

        user = db.execute('SELECT * FROM user WHERE email = ?', (email,)).fetchone()

        if user is None:
            error = 'Incorrect email entered'
        else:
            db.execute(
                'UPDATE user SET password = ? WHERE email = ?',
                (generate_password_hash(password), email)
            )
            db.commit()

        if error is None:
            # store the user id in a new session and return to the index
            session.clear()
            success = "Your account ({}) has been successfully changed its password!".format(email)
            flash(success, "success")
            return redirect(url_for('auth.login'))

        flash(error)
    return render_template('auth/change_password.html', datetime=datetime)


@bp.route('/reset', methods=['GET','POST'])
def reset():
    if g.user is not None:
        return redirect(url_for('food.index'))

    if request.method =='POST':
        db = get_db()
        error = None
        email = db.execute('SELECT * FROM user Where email = ?').fetchone()
        if email is None:
            error= 'No such user exists'
            flash(error)
            return render_template('auth/index.html')
    return render_template("auth/forgot_password.html", datetime=datetime)


@bp.route('/logout')
def logout():
    """Clear the current session, including the stored user id."""
    session.clear()
    return redirect(url_for('auth.login'))

