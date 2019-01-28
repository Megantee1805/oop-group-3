from flask import (Blueprint, flash, g, redirect, render_template, request, url_for)
from werkzeug.exceptions import abort
from datetime import datetime
from pytz import timezone
from tzlocal import get_localzone

from foodhubsg.auth import login_required
from foodhubsg.db import get_db
from foodhubsg.classes import *


def get_food_entry(id, check_user=True):
    db = get_db()
    food_entry = db.execute(
        'SELECT f.id, creator_id, food_name, datetime(created, "localtime"), calories, food_code, email'
        ' FROM food_entry f JOIN user u ON f.creator_id = u.id'
        ' WHERE f.id = ?',
        (id,),
    ).fetchone()

    if food_entry is None:
        abort(404, "That food entry (ID: {0}) doesn't exist".format(id))

    if check_user and food_entry['creator_id'] != g.user['id']:
        abort(403)

    return food_entry


bp = Blueprint('food', __name__)


@bp.route('/')
@login_required
def index():
    """Show all recent meals, most recent first."""
    db = get_db()
    food_items = db.execute(
        'SELECT f.id, creator_id, food_name, datetime(created, "localtime"), calories, food_code, email'
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
                           food_items=info["food_items"], calories_statement=info["calories_statement"], datetime=datetime)


@bp.route('/food_journal', methods=('GET', 'POST'))
@login_required
def food_journal():
    """Show all recent meals, most recent first."""
    db = get_db()
    food_items = db.execute(
        'SELECT f.id, creator_id, food_name, datetime(created, "localtime"), calories, food_code, email'
        ' FROM food_entry f JOIN user u ON f.creator_id = u.id'
        ' WHERE f.creator_id = ?'
        ' ORDER BY datetime(created, "localtime") DESC',
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

    now_utc = datetime.now(timezone('UTC'))
    now_local = now_utc.astimezone(get_localzone())

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
                           now=now_local, datetime=datetime)


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
            return redirect(url_for('food.edit_food', id=id))

    return render_template('food/edit_food.html', food_entry=food_entry, datetime=datetime)


@bp.route('/search_food/<search_date>', methods=('GET', 'POST'))
@login_required
def search_food(search_date):
    """Search a food entry if the current user is the creator"""
    db = get_db()
    current_date_food = []
    current_date_calories = []
    food_exists = 0

    try:
        display_date = datetime.strptime(search_date, '%Y-%m-%d').strftime('%d %B %Y (%A)')
        food_items = db.execute(
            'SELECT f.id, creator_id, food_name, datetime(created, "localtime"), calories, food_code, email'
            ' FROM food_entry f JOIN user u ON f.creator_id = u.id'
            ' WHERE f.creator_id = ? AND DATE(f.created) = ?',
            (g.user['id'], search_date,),
        ).fetchall()

        if food_items != []:
            food_exists = 1

        for food in food_items:
            current_date_food.append(food)
            current_date_calories.append(food['calories'])

        current_date_calories = sum(current_date_calories)

    except ValueError:
        abort(404, "That date ({0}) is invalid, please enter a date with a valid YYYY-MM-DD format.".format(search_date))

    return render_template('food/search_food.html', search_date=search_date, food_exists=food_exists, food_items=food_items,
                           current_date_calories=current_date_calories, display_date=display_date, datetime=datetime)
