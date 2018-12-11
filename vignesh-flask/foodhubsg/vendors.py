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


