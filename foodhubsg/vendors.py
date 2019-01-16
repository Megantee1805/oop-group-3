from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from foodhubsg.auth import login_required
from foodhubsg.db import get_db
from foodhubsg.classes import *
from foodhubsg.food import *


bp = Blueprint('vendors', __name__)


@bp.route('/vendors', methods=('GET', 'POST'))
def vendors():
    return render_template("vendors/vendor_page.html")

@bp.route('/vendors/<code>', methods=('GET', 'POST'))
def vendor(code):
    name = None
    average_calories = None
    area = None
    location = None
    description = None
    rating = None
    image_location = None

    if not [vendor for vendor in vendor_list if vendor.get_code() == code]:
        abort(404, "That vendor (code: {0}) doesn't exist.".format(code))

    else:
        for vendor in vendor_list:
            if vendor.get_code() == code:
                current_vendor = vendor
                name = current_vendor.get_name()
                average_calories = current_vendor.get_average_calories()
                area = current_vendor.get_area()
                location = current_vendor.get_location()
                description = current_vendor.get_description()
                rating = current_vendor.get_rating()
                image_location = current_vendor.get_image_location()

    return render_template("vendors/vendor.html", current_vendor=current_vendor, name=name,
                           average_calories=average_calories, area=area, location=location, description=description,
                           rating=rating, image_location=image_location)


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

    
    
for vendor in vendor_list:
        if user_location == vendor.get_location_code():
            user_vendors.append(vendor)
        else:
            continue

    return render_template('food/vendor_page.html',
                           food_dates=food_dates, all_dates=all_dates, calories_list=calories_list, name=name,
                           weight=weight, height=height, bmi=bmi, user_average_calories=user_average_calories,
                           number_of_days=number_of_days, food_exists=food_exists, user_vendors=user_vendors,
                           food_items=food_items, calories_statement=calories_statement)
