import sqlite3
import functools
from flask import (
    Flask, Blueprint, flash, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.exceptions import abort
from datetime import datetime

from foodhubsg.classes import Food, Vendor
from foodhubsg.db import *


support = 'support@foodhub.sg'
support_password = generate_password_hash('Iamasupport')


### AUTHORISATION CODE ###


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
        print(generate_password_hash(password))
        admin_login = False
        db = get_db()
        error = None
        user = db.execute(
            'SELECT * FROM user WHERE email = ?', (email,)
        ).fetchone()

        if email == support:
            if password == support_password:
                admin_login = True
                session.clear()
                session['user_id'] = user['id']
                redirect()

        if user is None:
            error = 'Incorrect email entered'
        else:
            if email == support:
                if check_password_hash(support_password, password):
                    admin_login = True
                    session.clear()
                    session['user_id'] = user['id']
                    return redirect(url_for('support.support'))
                else:
                    error = 'Incorrect password entered'
            else:
                if not check_password_hash(user['password'], password):
                    error = 'Incorrect password entered'

        if error is None:
            # store the user id in a new session and return to the index
            session.clear()
            session['user_id'] = user['id']
            return redirect(url_for('index'))

        else:
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
    return render_template('auth/change_password.html')


@bp.route('/reset', methods=['GET', 'POST'])
def reset():
    if g.user is not None:
        return redirect(url_for('food.index'))

    if request.method == 'POST':
        db = get_db()
        error = None
        email = db.execute('SELECT * FROM user Where email = ?').fetchone()
        if email is None:
            error = 'No such user exists'
            flash(error)
            return render_template('auth/index.html')
    return render_template("auth/forgot_password.html")


@bp.route('/logout')
def logout():
    """Clear the current session, including the stored user id."""
    session.clear()
    return redirect(url_for('auth.login'))


#### FOOD BLUEPRINT ###


bp = Blueprint('food', __name__)


@bp.route('/')
@login_required
def index():
    """Show all recent meals, most recent first."""
    db = get_db()
    food_items = db.execute(
        'SELECT f.id, creator_id, food_name, created, calories, food_code, email'
        ' FROM food_entry f JOIN user u ON f.creator_id = u.id'
        ' WHERE f.creator_id = ? AND DATE(f.created) IN'
        ' (SELECT DISTINCT DATE(created) FROM food_entry '
        ' WHERE NOT date(f.created) = date("now") ORDER BY datetime(created) DESC LIMIT 8)'
        ' ORDER BY datetime(created) DESC',
        (g.user['id'],),
    ).fetchall()

    users = db.execute(
        'SELECT id, name, email, password, height, weight, location'
        ' FROM user'
        ' WHERE id = ?',
        (g.user['id'],),
    ).fetchall()

    user_info = ProcessUserInfo(food_items, users)
    info = user_info.get_info()

    return render_template('food/index.html',
                           food_dates=info["food_dates"], all_dates=info["all_dates"], calories_list=info["calories_list"], name=info["name"],
                           weight=info["weight"], height=info["height"], bmi=info["bmi"], user_average_calories=info["user_average_calories"],
                           number_of_days=info["number_of_days"], food_exists=info["food_exists"], user_vendors=info["user_vendors"],
                           food_items=info["food_items"], calories_statement=info["calories_statement"])


@bp.route('/food_journal', methods=('GET', 'POST'))
@login_required
def food_journal():
    """Show all recent meals, most recent first."""
    db = get_db()
    food_items = db.execute(
        'SELECT f.id, creator_id, food_name, created, calories, food_code, email'
        ' FROM food_entry f JOIN user u ON f.creator_id = u.id'
        ' WHERE f.creator_id = ?'
        ' ORDER BY datetime(created) DESC',
        (g.user['id'],),
    ).fetchall()

    users = db.execute(
        'SELECT id, name, email, password, height, weight, location'
        ' FROM user'
        ' WHERE id = ?',
        (g.user['id'],),
    ).fetchall()

    user_info = ProcessUserInfo(food_items, users)
    info = user_info.get_info()

    if request.method == 'POST':
        error = None
        code_list = []

        if request.form['action'] == 'Save Food':
            code = request.form['code']
            code = code.lower()

            if not code:
                error = 'Code is required'

            else:
                db = get_db()
                for food in food_list:
                    food_code = food.get_code()
                    code_list.append(food_code)

                    if code == food_code:
                        food_calories = food.get_calories()
                        food_name = food.get_name()
                        db.execute(
                            'INSERT INTO food_entry (creator_id, food_code, food_name, calories)'
                            ' VALUES (?, ?, ?, ?)',
                            (g.user['id'], code, food_name, food_calories)
                        )
                        db.commit()
                        message = "Added {0} to your food journal!".format(food_name)
                        flash(message, "success")
                        return redirect(url_for('food.food_journal'))

                    else:
                        error = 'Invalid code entered'

        elif request.form['action'] == 'Search Date':
            search_date = request.form['search-date']
            return redirect(url_for('food.search_food', search_date=search_date))

        if error is not None:
            flash(error, "error")

    return render_template('food/food_journal.html', food_items=info["food_items"],
                           food_dates=info["food_dates"], all_dates=info["all_dates"],
                           calories_list=info["calories_list"], name=info["name"],
                           weight=info["weight"], height=info["height"], bmi=info["bmi"],
                           user_average_calories=info["user_average_calories"],
                           number_of_days=info["number_of_days"], food_exists=info["food_exists"],
                           now=datetime.utcnow())


@bp.route('/edit_food/<int:id>', methods=('GET', 'POST'))
@login_required
def edit_food(id):
    """Update a food entry if the current user is the creator"""
    db = get_db()
    food_entry = get_food_entry(id)
    old_food_name = food_entry['food_name']
    old_food_code = food_entry['food_code']

    if request.method == 'POST':
        if request.form['action'] == 'Update Entry':
            code = request.form['code']
            code = code.lower()
            error = None

            if not code:
                error = 'Please enter a code to edit your previous entry'

            elif code == old_food_code:
                error = "You've entered your previous code"

            else:
                for food in food_list:
                    food_code = food.get_code()

                    if code == food_code:
                        food_calories = food.get_calories()
                        food_name = food.get_name()
                        db.execute(
                            'UPDATE food_entry SET food_code = ?, food_name = ?, calories = ? WHERE id = ?',
                            (code, food_name, food_calories, id)
                        )
                        db.commit()
                        message = "Updated {0} ({1}) into {2} ({3}) for your food journal!".format(old_food_name, old_food_code, food_name, food_code)
                        flash(message, "success")
                        return redirect(url_for('food.food_journal'))
                    else:
                        error = 'Invalid code entered'

            if error is not None:
                flash(error, "error")

        elif request.form['action'] == 'Remove Food Entry':
            db.execute('DELETE FROM food_entry WHERE id = ?', (id,))
            db.commit()
            message = "Deleted {0} ({1}) from your food journal!".format(old_food_name, old_food_code)
            flash(message, "success")
            return redirect(url_for('food.food_journal'))

        else:
            return redirect(url_for('food.edit_food', id = id))

    return render_template('food/edit_food.html', food_entry=food_entry)


@bp.route('/search_food/<search_date>', methods=('GET', 'POST'))
@login_required
def search_food(search_date):
    """Search a food entry if the current user is the creator"""
    db = get_db()
    current_date_food = []
    current_date_calories = []

    try:
        display_date = datetime.strptime(search_date, '%Y-%m-%d').strftime('%d %B %Y (%A)')
        food_items = db.execute(
            'SELECT f.id, creator_id, food_name, created, calories, food_code, email'
            ' FROM food_entry f JOIN user u ON f.creator_id = u.id'
            ' WHERE f.creator_id = ? AND DATE(f.created) = ?',
            (g.user['id'], search_date,),
        ).fetchall()

        if food_items == []:
            food_exists = 0
        else:
            food_exists = 1

        for food in food_items:
            current_date_food.append(food)
            current_date_calories.append(food['calories'])

        current_date_calories = sum(current_date_calories)

    except ValueError:
        abort(404, "That date ({0}) is invalid, please enter a date with a valid YYYY-MM-DD format.".format(search_date))

    return render_template('food/search_food.html', search_date=search_date, food_exists=food_exists, food_items=food_items,
                           current_date_calories=current_date_calories, display_date=display_date)


#### USER BLUEPRINT ###


bp = Blueprint('user', __name__)


@bp.route('/user_settings', methods=('GET', 'POST'))
@login_required
def user_settings():
    db = get_db()
    food_items = db.execute(
        'SELECT f.id, creator_id, food_name, created, calories, food_code, email'
        ' FROM food_entry f JOIN user u ON f.creator_id = u.id'
        ' WHERE f.creator_id = ? AND DATE(f.created) IN'
        ' (SELECT DISTINCT DATE(created) FROM food_entry '
        ' WHERE NOT date(f.created) = date("now") ORDER BY datetime(created) DESC LIMIT 8)'
        ' ORDER BY datetime(created) DESC',
        (g.user['id'],),
    ).fetchall()

    users = db.execute(
        'SELECT id, name, email, password, height, weight, location'
        ' FROM user'
        ' WHERE id = ?',
        (g.user['id'],),
    ).fetchall()

    user_info = ProcessUserInfo(food_items, users)
    info = user_info.get_info()

    if request.method == 'POST':
        new_height = request.form['height']
        new_weight = request.form['weight']
        new_password = request.form['password']
        new_location = request.form.get('new-location')
        old_password = request.form['old-password']
        error = None
        message = None

        if new_height:
            if not 0.5 < float(new_height) < 2.5:
                error = 'Please enter a valid height value in meters'
            elif new_height == info["height"]:
                error = 'Please enter a new height value'
            else:
                db.execute(
                    'UPDATE user SET height = ? WHERE id = ?',
                    (new_height, info["id"])
                )

        if new_weight:
            if not 20 < float(new_weight) < 250:
                error = 'Please enter a valid weight value in kilograms'
            elif new_weight == info["weight"]:
                error = 'Please enter a new weight value'
            else:
                db.execute(
                    'UPDATE user SET weight = ? WHERE id = ?',
                    (new_weight, info["id"])
                )

        if new_location:
            db.execute(
                'UPDATE user SET location = ? WHERE id = ?',
                (new_location, info["id"])
            )
        else:
            error = "Previous location selected"

        if new_password:
            if old_password:
                if check_password_hash(info["password"], old_password):
                    if check_password_hash(info["password"], new_password):
                        error = "You've entered your previous password"
                    elif " " in  new_password:
                        error = "Please don't enter whitespaces in your new password"
                    else:
                        db.execute(
                            'UPDATE user SET password = ? WHERE id = ?',
                            (generate_password_hash(new_password), info["id"])
                        )
                else:
                    error = "You've entered your current password incorrectly"
            else:
                error = "Please enter your current password to change your password"

        if not new_height and not new_weight and not new_password and new_location == info["user_location"]:
            error = "No settings have been changed"

        if error is not None:
            flash(error, "error")
        else:
            message = "You've successfully changed your settings!"
            flash(message, "success")
            db.commit()
            return redirect(url_for('user.user_settings'))

    return render_template('user/user_settings.html',
                           name=info["name"], weight=info["weight"], height=info["height"], email=info["email"],
                           password=info["password"], user_location=info["user_location"], bmi_statement=info["bmi_statement"],
                           calories_statement=info["calories_statement"], number_of_days=info["number_of_days"],
                           user_average_calories=info["user_average_calories"], food_exists=info["food_exists"],
                           snack_message=info["snack_message"], average_breakfast_calories=info["average_breakfast_calories"],
                           average_lunch_calories=info["average_lunch_calories"], average_dinner_calories=info["average_dinner_calories"],
                           average_snack_calories=info["average_snack_calories"])


@bp.route('/faq', methods=('GET', 'POST'))
@login_required
def faq():
    db = get_db()
    if request.method == 'POST':
        if request.form['action'] == 'Submit A Question':
            question = request.form['query']
            print(request.form)
            answer = "No answer given yet, please answer on your own"
            if question is None or question == '':
                error = 'No value entered please try again'
                flash(error)
            else:
                db.execute('INSERT INTO question_and_answer (question, answer) VALUES (?, ?)', (question, answer))
                db.commit()
                queries = db.execute('SELECT id, question, answer FROM question_and_answer').fetchall()
                return render_template('user/faq.html', queries=queries)
        elif request.method == 'GET':
            if request.form['answer'] == 'Answer':
                qns = db.execute('SELECT question FROM question_and_answer WHERE id = ?', id).fetchone()
                return render_template('user/answer_faq.html', qns=qns)


        queries = db.execute('SELECT id, question, answer FROM question_and_answer').fetchall()
        # queries = list(map(lambda x: x[0], queries))
        # for row in queries:
        return render_template('user/faq.html', queries=queries)

# queries = list(map(lambda x: x[0], queries))

@bp.route('/answer/<int:id>', methods=('GET', 'POST'))
@login_required
def answer(id):
    db = get_db()
    qns = db.execute('SELECT question FROM question_and_answer WHERE id = ?', [id]).fetchone()
    if request.method == 'POST':
        if request.form['action'] == 'Submit Answer':
            answer = request.form['answer']
            if answer is None or answer == '':
                print(request.form)
                error = 'No value entered please try again'
                flash(error)
            else:
                db.execute('UPDATE question_and_answer SET answer= ? WHERE id = ?', (answer, id))
                db.commit()
                queries = db.execute('SELECT id, question, answer FROM question_and_answer').fetchall()
                return render_template('user/faq.html', queries=queries)
    return render_template('user/answer_faq.html', id=id, qns=qns[0])


#### VENDOR BLUEPRINT ###


bp = Blueprint('vendors', __name__)


@bp.route('/vendors', methods=('GET', 'POST'))
def vendors():
    db = get_db()

    users = db.execute(
        'SELECT id, name, email, password, height, weight, location'
        ' FROM user'
        ' WHERE id = ?',
        (g.user['id'],),
    ).fetchall()

    for user in users:
        user_location = user['location']

    user_vendors = []
    for vendors in vendor_list:
        vendor = vendor_list[vendors]
        if user_location == vendor.get_area():
                user_vendors.append(vendor)
        else:
            continue

    return render_template("vendors/vendor_page.html", user_vendors=user_vendors)


@bp.route('/vendors/<code>', methods=('GET', 'POST'))
def vendor(code):
    name = None
    average_calories = None
    area = None
    location = None
    description = None
    rating = None
    image_location = None

    for vendors in vendor_list:
        vendor = vendor_list[vendors]
        if vendor.get_code() == code:
            if not vendor:
                abort(404, "That vendor (code: {0}) doesn't exist.".format(code))

    else:
        for vendors in vendor_list:
            vendor = vendor_list[vendors]
            if vendor.get_code() == code:
                current_vendor = vendor
                name = current_vendor.get_name()
                average_calories = current_vendor.get_average_calories()
                area = current_vendor.get_area()
                location = current_vendor.get_location()
                description = current_vendor.get_description()
                rating = current_vendor.get_rating()
                image_location = current_vendor.get_image_location()

                for key, value in vendor_food.items():
                    if key.get_code() == code:
                        vendor_food_list = value

                return render_template("vendors/vendor.html", current_vendor=current_vendor, name=name,
                                           average_calories=average_calories, area=area, location=location, description=description,
                                           rating=rating, image_location=image_location, vendor_food_list=vendor_food_list)


### SUPPORT BLUEPRINT ###


bp = Blueprint('support', __name__)


@bp.route('/support')
@login_required
def support():
    admin_login= True
    return render_template('support/support_index.html', admin_login=True)


@bp.route('/support_faq')
@login_required
def faq():
    db = get_db()
    if g.user == 'support@foodhub.sg':
        admin_login = True
        if request.method == 'POST':
            if request.form['action'] == 'Submit A Question':
                question = request.form['query']
                print(request.form)
                answer = "No answer given yet, please answer on your own"
                if question is None or question == '':
                    error = 'No value entered please try again'
                    flash(error)
                else:
                    db.execute('INSERT INTO question_and_answer (question, answer) VALUES (?, ?)', (question, answer))
                    db.commit()
                    queries = db.execute('SELECT id, question, answer FROM question_and_answer').fetchall()
        if request.method == "GET":
            if request.form['answer'] == 'Answer':
                qns = db.execute('SELECT question FROM question_and_answer WHERE id = ?', id).fetchone()
                return render_template('user/answer_faq.html', qns=qns)
            elif request.form['delete'] == 'Delete':
                db.execute('DELETE FROM question_and_answer WHERE id = ?', id).fetchone()
                return render_template('user/faq.html', admin_login=admin_login)
