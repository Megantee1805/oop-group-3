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


@bp.route('/faq', methods=('GET', 'POST'))
@permission_required
def faq():
    db = get_db()
    if request.method == 'POST':
        if request.form['action'] == 'Submit A Question':
            question = request.form['query']
            print(request.form)
            answer = "No answer given yet, please answer on your own"
            if question is None or question == '':
                error = 'No value entered please try again'
                flash(error)
            else:
                db.execute('INSERT INTO question_and_answer (question, answer) VALUES (?, ?)', (question, answer))
                db.commit()
                queries = db.execute('SELECT id, question, answer FROM question_and_answer').fetchall()
    if request.method == "GET":
        if request.form['answer'] == 'Answer':
            qns = db.execute('SELECT question FROM question_and_answer WHERE id = ?', id).fetchone()
            return render_template('user/answer_faq.html', qns=qns)
        elif request.form['delete'] == 'Delete':
            db.execute('DELETE FROM question_and_answer WHERE id = ?', id)
            db.commit()
            return render_template('user/faq.html')
    return render_template('user/faq.html')


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
