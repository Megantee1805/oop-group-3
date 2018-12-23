from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort
from werkzeug.security import check_password_hash, generate_password_hash

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


bp = Blueprint('user', __name__)


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
        id = user['id']
        name = user['name']
        weight = user['weight']
        height = user['height']
        email = user['email']
        password = user['password']

    bmi = weight / height ** height
    bmi = int(bmi)

    all_dates = []
    food_dates = []
    calories_list = []
    user_average_calories = 0
    number_of_days = 0

    if food_items is not []:
        food_exists = 1
    else:
        food_exists = 0

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

        user_average_calories = int(sum(calories_list) / number_of_days)

    if request.method == 'POST':
        new_name = request.form['name']
        new_height = request.form['height']
        new_weight = request.form['weight']
        new_password = request.form['password']
        error = None

        db = get_db()

        try:
            if new_name:
                if not all(char.isalpha() or char.isspace() for char in new_name):
                    error = 'Please only enter alphabets for your name'
                elif not len(new_name) < 16:
                    error = 'Please enter a name below 16 characters'
                elif new_name.title() == name:
                    error ='Please enter a new name'
                else:
                    db.execute(
                        'UPDATE user SET name = ? WHERE id = ?',
                        (new_name.title(), id)
                    )

            if new_height:
                if not 0.5 < float(new_height) < 2.5:
                    error = 'Please enter a valid height value in meters'
                elif new_height == height:
                    error ='Please enter a new height value'
                else:
                    db.execute(
                        'UPDATE user SET height = ? WHERE id = ?',
                        (new_height, id)
                    )

            if new_weight:
                if not 20 < float(new_weight) < 250:
                    error = 'Please enter a valid weight value in kilograms'
                elif new_weight == weight:
                    error ='Please enter a new weight value'
                else:
                    db.execute(
                        'UPDATE user SET weight = ? WHERE id = ?',
                        (new_weight, id)
                    )

            if new_password:
                db.execute(
                    'UPDATE user SET password = ? WHERE id = ?',
                    (generate_password_hash(new_password), id)
                )
                message = "You've successfully changed your password!"
                flash(message, "success")

        except ValueError:
            error = "Please enter a valid value"

        if error is not None:
            flash(error, "error")

        else:
            db.commit()
            return redirect(url_for('user.user_settings'))

    return render_template('user/user_settings.html',
                           name=name, weight=weight, height=height, email=email, password=password, bmi=bmi,
                           user_average_calories=user_average_calories, number_of_days=number_of_days,
                           food_exists=food_exists)
