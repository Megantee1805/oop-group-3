import functools
from flask import (
    Blueprint, flash, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

from foodhubsg.db import *
# from flask_mail import Message, Mail

# mail = Mail()

def remove_duplicates(values):
    output = []
    seen = set()
    for value in values:
        if value not in seen:
            output.append(value)
            seen.add(value)
    return output


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
    if g.user is not None:
        return redirect(url_for('food.index'))

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
        elif " " in password:
            error = "Please don't enter whitespaces in your password"
        elif check_user is not None:
            error = 'This email ({}) is already registered.'.format(email)

        name = name.title()
        email = email.lower()
        location = "Ang Mo Kio"

        if error is None:
            db.execute(
                'INSERT INTO user (email, password, name, height, weight, location) VALUES (?, ?, ?, ?, ?, ?)',
                (email, generate_password_hash(password), name, height, weight, location)
            )
            db.commit()

            success = "Your account ({}) has been successfully registered!".format(email)
            flash(success, "success")

            return redirect(url_for('auth.login'))

        else:
            flash(error)

    return render_template('auth/register.html')


@bp.route('/login', methods=('GET', 'POST'))
def login():
    """Log in a registered user by adding the user id to the session."""
    if g.user is not None:
        return redirect(url_for('food.index'))

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

    return render_template('auth/change_password.html')

#
# @bp.route('/confirm')
# def confirm():
#     db = get_db()
#     email = db.execute('SELECT * FROM user Where email = ?').fetchone()
#     if email is None:
#         error = 'Registration was not succeasful'
#         flash(error)
#         return render_template('auth/index.html')
#     else:
#         msg = Message("Hello",
#                       sender="Megan.tee1805@gmail.com",
#                       recipients=[email])
#         mail.send(msg)
#         return render_template('auth/verification_email.html')

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
        else:
            msg = Message(
                "Click here to change your password",
                recipients=email
            )
            mail.send(msg)
    return render_template("auth/forgot_password.html")

@bp.route('/logout')
def logout():
    """Clear the current session, including the stored user id."""
    session.clear()
    return redirect(url_for('auth.login'))

