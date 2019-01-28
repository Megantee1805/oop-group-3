from flask import (Blueprint, flash, g, redirect, render_template, request, url_for)
from werkzeug.exceptions import abort
from datetime import datetime

from foodhubsg.auth import login_required
from foodhubsg.db import get_db
from foodhubsg.classes import *


bp = Blueprint('vendors', __name__)


@bp.route('/vendors', methods=('GET', 'POST'))
@login_required
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

    return render_template("vendors/vendor_page.html", user_vendors=user_vendors, datetime=datetime)


@bp.route('/vendors/<code>', methods=('GET', 'POST'))
def vendor(code):
    if code not in vendor_list:
        abort(404, "That vendor (code: {0}) doesn't exist.".format(code))

    else:
        for vendor_code in vendor_list:
            vendor = vendor_list[vendor_code]
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
                                           rating=rating, image_location=image_location, vendor_food_list=vendor_food_list, datetime=datetime)
