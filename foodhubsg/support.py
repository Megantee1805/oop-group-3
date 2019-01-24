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
    # db = get_db()
    # if request.method == 'POST':
    #     if request.form['action'] == 'Submit A Question':
    #         question = request.form['query']
    #         print(request.form)
    #         answer = "No answer given yet, please answer on your own"
    #         if question is None or question == '':
    #             error = 'No value entered please try again'
    #             flash(error)
    #         else:
    #             db.execute('INSERT INTO question_and_answer (question, answer) VALUES (?, ?)', (question, answer))
    #             db.commit()
    #             queries = db.execute('SELECT id, question, answer FROM question_and_answer').fetchall()
    # if request.method == "GET":
    #     if request.form['answer'] == 'Answer':
    #         qns = db.execute('SELECT question FROM question_and_answer WHERE id = ?', id).fetchone()
    #         return render_template('user/answer_faq.html', qns=qns)
    #     elif request.form['delete'] == 'Delete':
    #         db.execute('DELETE FROM question_and_answer WHERE id = ?', id)
    #         db.commit()
    return render_template('support/support_index.html')


@bp.route('/support_faq')
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
            return render_template('user/faq.html', admin_login=admin_login)

