from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from foodhubsg.auth import login_required
from foodhubsg.db import get_db
from foodhubsg.classes import *
from foodhubsg.vendors import *


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
    user_vendors = []
    user_average_calories = 0
    number_of_days = 0
    user_location = "sen"


    if food_items is []:
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

    for vendor in vendor_list:
        if user_location == vendor.get_location_code():
            user_vendors.append(vendor)
        else:
            continue

    return render_template('food/index.html',
                           food_dates=food_dates, all_dates=all_dates, calories_list=calories_list, name=name,
                           weight=weight, height=height, bmi=bmi, user_average_calories=user_average_calories,
                           number_of_days=number_of_days, food_exists=food_exists, user_vendors=user_vendors, food_items=food_items)


@bp.route('/food_journal', methods=('GET', 'POST'))
@login_required
def food_journal():
    """Show all recent meals, most recent first."""
    db = get_db()
    food_items = db.execute(
        'SELECT f.id, creator_id, food_name, created, calories, food_code, email'
        ' FROM food_entry f JOIN user u ON f.creator_id = u.id'
        ' WHERE f.creator_id = ? AND f.created > (SELECT DATETIME("now", "-3 day"))'
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

    all_dates = []
    food_dates = []
    calories_list = []
    user_average_calories = 0
    number_of_days = 0

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


@bp.route('/add', methods=('GET', 'POST'))
@login_required
def add_food():
    """Create a new food entry for the current user."""
    if request.method == 'POST':
        code = request.form['code']
        error = None

        if not code:
            error = 'Code is required'

        else:
            db = get_db()
            for food in food_list:
                food_code = food.get_code()

                if code == food_code:
                    error = None
                    food_calories = food.get_calories()
                    food_name = food.get_name()
                    db.execute(
                        'INSERT INTO food_entry (creator_id, food_code, food_name, calories)'
                        ' VALUES (?, ?, ?, ?)',
                        (g.user['id'], code, food_name, food_calories)
                    )
                    db.commit()
                    return redirect(url_for('food.food_journal'))
                else:
                    error = 'Invalid code entered'

        if error is not None:
            flash(error)

    return render_template('food/food_journal.html')


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
