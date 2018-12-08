# from flask import (
#     Blueprint, flash, g, redirect, render_template, request, url_for
# )
# from werkzeug.exceptions import abort
#
# from foodhubsg.auth import login_required
# from foodhubsg.db import get_db
# from foodhubsg.classes import *


def remove_duplicates(values):
    output = []
    seen = set()
    for value in values:
        if value not in seen:
            output.append(value)
            seen.add(value)
    return output


# db = get_db()
# food_items = db.execute(
#     'SELECT f.id, creator_id, food_name, created, calories, food_code, email'
#     ' FROM food_entry f JOIN user u ON f.creator_id = u.id'
#     ' WHERE f.creator_id = ?',
#     (g.user['id'],)
# ).fetchall()


all_dates = []
food_dates = []


for food in food_items:
    food_date = food['created'].strftime('%Y-%m-%d')
    all_dates.append(food_date)
remove_duplicates(all_dates)

for food_date in all_dates:
    current_date_food = []
    for food in food_items:
        if food['created'].strftime('%Y-%m-%d') == food_date:
            current_date_food.append(food)
        else:
            continue
        food_dates.append(current_date_food)

print(food_dates)
