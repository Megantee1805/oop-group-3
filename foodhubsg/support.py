from flask import (Blueprint, flash, redirect, render_template, request, session, url_for)
from collections import OrderedDict
import operator

from foodhubsg.auth import permission_required
from foodhubsg.db import get_db
from foodhubsg.classes import *


bp = Blueprint('support', __name__)


@bp.route('/support')
@permission_required
def support():
    db = get_db()
    food_items = db.execute('SELECT * FROM food_entry').fetchall()
    support_data = SupportData()
    for food in food_items:
        support_data.add_food(food)
    food_dict = support_data.get_food_menu()
    sorted_food_dict = sorted(food_dict.items(), key=operator.itemgetter(1), reverse=True)

    return render_template('support/support_index.html', food_dict=sorted_food_dict)
    most_common_food =sorted_food_dict[:3]
    return render_template('support/support_index.html', food_dict=most_common_food)


@bp.route('/support_faq', methods=('GET', 'POST'))
@permission_required
def support_faq():
    db = get_db()
    queries = db.execute('SELECT * FROM question_and_answer').fetchall()
    if request.method == 'POST':
        if request.form['answer'] == 'Edit':
            qns = db.execute('SELECT question FROM question_and_answer WHERE id = ?', id).fetchone()
            return render_template('support/edit_faq.html', qns=qns)
    return render_template('support/support_faq.html', queries=queries)


@bp.route('/edit_faq/<int:id>', methods=('GET', 'POST'))
@permission_required
def edit_faq(id):
    db = get_db()
    qns = db.execute('SELECT question FROM question_and_answer WHERE id = ?', [id]).fetchone()
    ans = db.execute('SELECT answer FROM question_and_answer WHERE id = ?', [id]).fetchone()
    if request.method == 'POST':
        if request.form['action'] == 'Submit Answer':
            answer = request.form['answer']
            if answer is None or answer == '':
                error = 'No value entered please try again'
                flash(error)
            else:
                db.execute('UPDATE question_and_answer SET answer= ? WHERE id = ?', (answer, id))
                db.commit()
                return redirect(url_for('support.support_faq'))

        elif request.form['action'] == 'Delete Question':
            db.execute('DELETE FROM question_and_answer WHERE id = ?', (id,))
            db.commit()
            return redirect(url_for('support.support_faq'))

    return render_template('support/edit_faq.html', id=id, qns=qns[0], ans=ans)


@bp.route('/ban_user', methods=('GET', 'POST'))
@permission_required
def ban_user():
    db= get_db()
    users = db.execute('SELECT * FROM user').fetchall()
    if request.method == 'POST':
        if request.form['action'] == 'Ban User':
            name = request.form['name']
            db.execute('UPDATE user SET status = ? WHERE name = ?', (1, name))
            db.commit()
            message = 'Banned the user succesfully'
            users = db.execute('SELECT * FROM user').fetchall()
            flash(message, "success")
            return render_template('support/ban_users.html', users=users)
        elif request.form['action'] == 'Unban User':
            name = request.form['name']
            db.execute('UPDATE user SET status = ? WHERE name = ?', (0, name))
            db.commit()
            message = 'The user is now free to post'
            users = db.execute('SELECT * FROM user').fetchall()
            flash(message, "success")
            return render_template('support/ban_users.html', users=users)

    return render_template('support/ban_users.html', users=users)
