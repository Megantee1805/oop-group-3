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

    for vendor in vendor_list:
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


