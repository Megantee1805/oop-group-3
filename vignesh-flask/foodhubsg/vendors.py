from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from foodhubsg.auth import login_required
from foodhubsg.db import get_db
from foodhubsg.classes import *


def remove_duplicates(values):
    output = []
    seen = set()
    for value in values:
        if value not in seen:
            output.append(value)
            seen.add(value)
    return output


bp = Blueprint('vendors', __name__)

@bp.route('/food_journal')
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
        email = user['email']
        password = user['password']

    bmi = weight / height ** height
    bmi = int(bmi)

    all_dates = []
    food_dates = []
    calories_list = []

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

    return render_template('food/food_journal.html',
                           food_dates=food_dates, all_dates=all_dates, calories_list=calories_list, name=name,
                           weight=weight, height=height, bmi=bmi)

@login_required
@bp.route('/vendors')
def vendors():
    for location in locations:
        for vendors in location:
            name = vendors.get_name()
            location = vendors.get_location()
            calories = vendors.get_average_calories()
            description = vendors.get_description()
            return render_template("food/vendor.html", vendors=vendors, name=name, location=location, calories=calories,
                                   description=description)


