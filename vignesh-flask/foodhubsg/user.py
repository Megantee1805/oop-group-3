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

    bmi = round(bmi, 2)
    all_dates = []
    food_dates = []
    calories_list = []
    breakfast_list = []
    lunch_list = []
    dinner_list = []
    snack_list = []
    user_average_calories = None
    number_of_days = None
    average_breakfast_calories = None
    average_lunch_calories = None
    average_dinner_calories = None
    average_snack_calories = None
    calories_statement = None
    breakfast_message = None
    lunch_message = None
    dinner_message = None
    snack_message = None
    ideal_weight = weight
    password_placeholder = "(unchanged)"

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

        user_average_calories = int(sum(calories_list) / number_of_days)

    for food in food_items:
        if 5 <= int(food['created'].strftime('%-H')) <= 10:
            breakfast_list.append(food['calories'])
            average_breakfast_calories = sum(breakfast_list) / number_of_days
        elif 11 <= int(food['created'].strftime('%-H')) <= 14:
            lunch_list.append(food['calories'])
            average_lunch_calories = sum(lunch_list) / number_of_days
        elif 17 <= int(food['created'].strftime('%-H')) <= 22:
            dinner_list.append(food['calories'])
            average_dinner_calories = sum(dinner_list) / number_of_days
        else:
            snack_list.append(food['calories'])
            average_snack_calories = sum(snack_list) / number_of_days


    if bmi < 22:
        while ideal_weight / height ** height < 23:
            ideal_weight = ideal_weight + 1
        lose_weight = ideal_weight - weight
        bmi_statement = "{}, you have a BMI of {}, which is below the healthy range of 22 to 24. You are recommended " \
                        "to gain {} kg to reach a body mass of {} kg, which will get you back to the healthy BMI range." \
                        .format(name, bmi, lose_weight, ideal_weight)
    elif 22 < bmi < 24:
        bmi_statement = "{}, you have a BMI of {}, which is exactly within the healthy BMI range. " \
                        "Keep it up!".format(name, bmi)

    elif bmi > 24:
        while ideal_weight / height ** height > 23:
            ideal_weight = ideal_weight - 1
        lose_weight = weight - ideal_weight
        bmi_statement = "{}, you have a BMI of {}, which is above the healthy range of 22 to 24. You are recommended " \
                        "to lose {} kg to reach a body mass of {} kg, which will get you back to the healthy BMI range." \
                        .format(name, bmi, lose_weight, ideal_weight)

    if user_average_calories:
        if user_average_calories < 2000:
            calories_statement = "You consumed an average of {} kcal daily over the past {} days, " \
                                 "which is below the daily recommended amount of 2500 kcal."\
                                .format(user_average_calories, number_of_days)
        elif 2000 < user_average_calories < 3000:
            calories_statement = "You consumed an average of {} kcal daily over the past {} days, " \
                                 "which is within the daily recommended amount, so keep following your current diet." \
                                .format(user_average_calories, number_of_days)

        elif 2000 < user_average_calories < 3000:
            calories_statement = "You consumed an average of {} kcal daily over the past {} days, " \
                                 "which is above the daily recommended amount of 2500 kcal." \
                                .format(user_average_calories, number_of_days)

    if average_breakfast_calories:
        if average_breakfast_calories < 350:
            breakfast_message = "You need to increase your breakfast calories."
        elif average_breakfast_calories > 500:
            breakfast_message = "You need to decrease your breakfast calories."

    if average_lunch_calories:
        if average_lunch_calories < 650:
            lunch_message = "You need to increase your lunch calories."
        elif average_lunch_calories > 850:
            lunch_message = "You need to decrease your lunch calories."

    if average_dinner_calories:
        if average_dinner_calories < 275:
            dinner_message = "You need to increase your dinner calories."
        elif average_dinner_calories > 350:
            dinner_message = "You need to decrease your dinner calories."

    if average_snack_calories:
        if average_snack_calories > 300:
            snack_message = "You need to decrease your out-of-schedule snack intake."

    messages = [breakfast_message, lunch_message, dinner_message, snack_message]

    messages = list(filter(None.__ne__, messages))

    if messages == []:
        messages = "You have not added any food to the journal yet."

    if request.method == 'POST':
        new_name = request.form['name']
        new_height = request.form['height']
        new_weight = request.form['weight']
        new_password = request.form['password']
        error = None
        message = None

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
                if check_password_hash(password, new_password):
                    error = "You've entered your previous password"
                else:
                    db.execute(
                        'UPDATE user SET password = ? WHERE id = ?',
                        (generate_password_hash(new_password), id)
                    )
                    password_placeholder = "(changed)"

            if not new_name and not new_height and not new_weight and not new_password:
                error = "No settings have been changed"

        except ValueError:
            error = "Please enter a valid value"

        if error is not None:
            flash(error, "error")
        else:
            message = "You've successfully changed your settings!"
            flash(message, "success")
            db.commit()
            return redirect(url_for('user.user_settings'))

    return render_template('user/user_settings.html',
                           name=name, weight=weight, height=height, email=email, password=password, bmi_statement=bmi_statement,
                           calories_statement=calories_statement, number_of_days=number_of_days,
                           food_exists=food_exists, password_placeholder=password_placeholder, messages=messages)
