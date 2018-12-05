from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from foodhubsg.auth import login_required
from foodhubsg.db import get_db
from foodhubsg.classes import *


bp = Blueprint('food', __name__)

@bp.route('/')
@login_required
def index():
    """Show all the posts, most recent first."""
    db = get_db()
    food_items = db.execute(
        'SELECT f.id, creator_id, food_name, created, calories, food_code, email'
        ' FROM food_entry f JOIN user u ON f.creator_id = u.id'
        ' WHERE f.creator_id = ?',
        (g.user['id'],)
    ).fetchall()
    return render_template('food/index.html', food_items=food_items)


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
                    return redirect(url_for('food.index'))
                else:
                    error = 'Invalid code entered'

        if error is not None:
            flash(error)

    return render_template('food/add_food.html')


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
