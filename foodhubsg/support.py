import functools
from flask import (
    Blueprint, flash, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

from foodhubsg.db import *
from foodhubsg.auth import login_required, permission_required
from foodhubsg.db import *
from foodhubsg.classes import *
from foodhubsg.vendors import *
bp = Blueprint('support', __name__)


@bp.route('/support')
@permission_required
def support():
    db = get_db()
    id = 1
    while id > 0:
        food = db.execute('SELECT food_code, food_name FROM food_entry WHERE id = ?', [id]).fetchone()
        food_data = Data()
        food_code = food[0]
        food_name = food[1]
        food_data.add_food(food_code)
        food_items = food_data.get_food_dict(food_name, food_code)
        id = id + 1
        return render_template('support/support_index.html', items=food_items)


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
