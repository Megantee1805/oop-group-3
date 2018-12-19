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


bp = Blueprint('user', __name__)


@bp.route('/user_settings', methods=('GET', 'POST'))
@login_required
def user_settings(id):
    if request.method == 'POST':
        db = get_db()
        food_items = db.execute(
            'SELECT f.id, creator_id, food_name, created, calories, food_code, email'
            ' FROM food_entry f JOIN user u ON f.creator_id = u.id'
            ' WHERE f.creator_id = ?' # add "AND f.created BETWEEN ? AND ?" to the where statement to filter between dates
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

        title = request.form['title']
        body = request.form['body']
        error = None

        if not title:
            error = 'Title is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'UPDATE post SET title = ?, body = ? WHERE id = ?',
                (title, body, id)
            )
            db.commit()
            return redirect(url_for('blog.index'))

    return render_template('user_settings.html', name=name, height=height, weight=weight)
