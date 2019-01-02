from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from foodhubsg.auth import login_required
from foodhubsg.db import get_db
from foodhubsg.classes import *
from foodhubsg.vendors import *


def get_food_entry(id, check_user=True):
    db = get_db()
    food_entry = db.execute(
        'SELECT f.id, creator_id, food_name, created, calories, food_code, email'
        ' FROM food_entry f JOIN user u ON f.creator_id = u.id'
        ' WHERE f.id = ?',
        (id,),
    ).fetchone()

    if food_entry is None:
        abort(404, "That food entry (ID: {0}) doesn't exist".format(id))

    if check_user and food_entry['creator_id'] != g.user['id']:
        abort(403)

    return food_entry

def remove_duplicates(values):
    output = []
    seen = set()
    for value in values:
        if value not in seen:
            output.append(value)
            seen.add(value)
    return output


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
        ' (SELECT DISTINCT DATE(created) FROM food_entry ORDER BY datetime(created) DESC LIMIT 6)',
        (g.user['id'],),
    ).fetchall()

    users = db.execute(
        'SELECT id, name, email, password, height, weight'
        ' FROM user'
        ' WHERE id = ?',
        (g.user['id'],),
    ).fetchall()

    for user in users:
        weight = user['weight']
        height = user['height']
        name = user['name']

    bmi = weight / height ** height

    bmi = round(bmi, 2)
    all_dates = []
    food_dates = []
    user_vendors = []
    calories_list = []
    user_average_calories = None
    number_of_days = None
    calories_statement = None
    user_location = "sen"

    if food_items == []:
        food_exists = 0
    else:
        food_exists = 1

    for food in food_items:
        food_date = food['created'].strftime('%d-%m-%y')
        all_dates.append(food_date)
    all_dates = remove_duplicates(all_dates)

    for date in all_dates:
        current_date_food = []
        current_date_calories = []

        for food in food_items:
            if date == food['created'].strftime('%d-%m-%y'):
                current_date_food.append(food)
                current_date_calories.append(food['calories'])
            else:
                continue
        food_dates.append(current_date_food)
        current_date_calories = sum(current_date_calories)
        calories_list.append(current_date_calories)

        number_of_days = len(calories_list)

        user_average_calories = int(sum(calories_list)/number_of_days)

    if user_average_calories:
        if user_average_calories < 2000:
            calories_statement = "{0}, you consumed an average of {1} kcal daily over the last {2} days you've entered food " \
                                 "into your food journal, which is below the daily recommended amount of 2500 kcal."\
                                .format(name, user_average_calories, number_of_days)
        elif 2000 < user_average_calories < 3000:
            calories_statement = "{0}, you consumed an average of {1} kcal daily over the {2} days you've entered food " \
                                 "into your food journal, which is within the daily recommended amount, so keep following your current diet!" \
                                .format(name, user_average_calories, number_of_days)

        elif 2000 < user_average_calories < 3000:
            calories_statement = "{0}, you consumed an average of {1} kcal daily over the last {2} days you've entered food " \
                                 "into your food journal, which is above the daily recommended amount of 2500 kcal." \
                                .format(name, user_average_calories, number_of_days)

    else:
        calories_statement = "You have not added any food to the journal yet, so there isn't a summary available yet!"

    for vendor in vendor_list:
        if user_location == vendor.get_location_code():
            user_vendors.append(vendor)
        else:
            continue

    return render_template('food/index.html',
                           food_dates=food_dates, all_dates=all_dates, calories_list=calories_list, name=name,
                           weight=weight, height=height, bmi=bmi, user_average_calories=user_average_calories,
                           number_of_days=number_of_days, food_exists=food_exists, user_vendors=user_vendors,
                           food_items=food_items, calories_statement=calories_statement)

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
        'SELECT id, name, email, password, height, weight'
        ' FROM user'
        ' WHERE id = ?',
        (g.user['id'],),
    ).fetchall()

    for user in users:
        weight = user['weight']
        height = user['height']
        name = user['name']

    bmi = weight / height ** height

    bmi = int(bmi)
    all_dates = []
    food_dates = []
    calories_list = []
    user_average_calories = 0
    number_of_days = 0

    if request.method == 'POST':
        code = request.form['code']
        code = code.lower()
        error = None

        if not code:
            error = 'Code is required'

        else:
            db = get_db()
            for food in food_list:
                food_code = food.get_code()

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

        if error is not None:
            flash(error, "error")

    if food_items == []:
        food_exists = 0
    else:
        food_exists = 1

    for food in food_items:
        food_date = food['created'].strftime('%d-%m-%y')
        all_dates.append(food_date)
    all_dates = remove_duplicates(all_dates)

    for date in all_dates:
        current_date_food = []
        current_date_calories = []

        for food in food_items:
            if date == food['created'].strftime('%d-%m-%y'):
                current_date_food.append(food)
                current_date_calories.append(food['calories'])
            else:
                continue

        food_dates.append(current_date_food)
        current_date_calories = sum(current_date_calories)
        calories_list.append(current_date_calories)

        number_of_days = len(calories_list)

        user_average_calories = int(sum(calories_list)/number_of_days)

    return render_template('food/food_journal.html',
                           food_dates=food_dates, all_dates=all_dates, calories_list=calories_list, name=name,
                           weight=weight, height=height, bmi=bmi, user_average_calories=user_average_calories,
                           number_of_days=number_of_days, food_exists=food_exists)


@bp.route('/<int:id>/edit_food', methods=('GET', 'POST'))
@login_required
def edit_food(id):
    """Update a food entry if the current user is the creator"""
    db = get_db()
    food_entry = get_food_entry(id)
    old_food_name = food_entry['food_name']
    old_food_code = food_entry['food_code']

    if request.method == 'POST':
        if request.form['action'] == 'Edit Food Code':
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

    return render_template('food/edit_food.html', food_entry=food_entry)


@bp.route('/faq', methods=('GET', 'POST'))
@login_required
def faq():
    return render_template('food/faq.html')


# def get_post(id, check_author=True):
#     """Get a post and its author by id.
#
#     Checks that the id exists and optionally that the current user is
#     the author.
#
#     :param id: id of post to get
#     :param check_author: require the current user to be the author
#     :return: the post with author information
#     :raise 404: if a post with the given id doesn't exist
#     :raise 403: if the current user isn't the author
#     """
#     post = get_db().execute(
#         'SELECT p.id, title, body, created, author_id, email'
#         ' FROM post p JOIN user u ON p.author_id = u.id'
#         ' WHERE p.id = ?',
#         (id,)
#     ).fetchone()
#
#     if post is None:
#         abort(404, "Post id {0} doesn't exist.".format(id))
#
#     if check_author and post['author_id'] != g.user['id']:
#         abort(403)
#
#     return post
#
#
# @bp.route('/<int:id>/update', methods=('GET', 'POST'))
# @login_required
# def update(id):
#     """Update a post if the current user is the author."""
#     post = get_post(id)
#
#     if request.method == 'POST':
#         title = request.form['title']
#         body = request.form['body']
#         error = None
#
#         if not title:
#             error = 'Title is required.'
#
#         if error is not None:
#             flash(error)
#         else:
#             db = get_db()
#             db.execute(
#                 'UPDATE post SET title = ?, body = ? WHERE id = ?',
#                 (title, body, id)
#             )
#             db.commit()
#             return redirect(url_for('blog.index'))
#
#     return render_template('blog/update.html', post=post)
#
#
# @bp.route('/<int:id>/delete', methods=('POST',))
# @login_required
# def delete(id):
#     """Delete a post.
#
#     Ensures that the post exists and that the logged in user is the
#     author of the post.
#     """
#     get_post(id)
#     db = get_db()
#     db.execute('DELETE FROM post WHERE id = ?', (id,))
#     db.commit()
#     return redirect(url_for('blog.index'))