from werkzeug.security import check_password_hash, generate_password_hash
from foodhubsg.vendors import *
import sqlite3


bp = Blueprint('user', __name__)


@bp.route('/user_settings', methods=('GET', 'POST'))
@login_required
def user_settings():
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

    users = db.execute(
        'SELECT id, name, email, password, height, weight, location'
        ' FROM user'
        ' WHERE id = ?',
        (g.user['id'],),
    ).fetchall()

    user_info = ProcessUserInfo(food_items, users)
    info = user_info.get_info()

    if request.method == 'POST':
        new_height = request.form['height']
        new_weight = request.form['weight']
        new_password = request.form['password']
        new_location = request.form.get('new-location')
        old_password = request.form['old-password']
        error = None
        message = None

        if new_height:
            if not 0.5 < float(new_height) < 2.5:
                error = 'Please enter a valid height value in meters'
            elif new_height == info["height"]:
                error = 'Please enter a new height value'
            else:
                db.execute(
                    'UPDATE user SET height = ? WHERE id = ?',
                    (new_height, info["id"])
                )

        if new_weight:
            if not 20 < float(new_weight) < 250:
                error = 'Please enter a valid weight value in kilograms'
            elif new_weight == info["weight"]:
                error = 'Please enter a new weight value'
            else:
                db.execute(
                    'UPDATE user SET weight = ? WHERE id = ?',
                    (new_weight, info["id"])
                )

        if new_location:
            db.execute(
                'UPDATE user SET location = ? WHERE id = ?',
                (new_location, info["id"])
            )
        else:
            error = "Previous location selected"

        if new_password:
            if old_password:
                if check_password_hash(info["password"], old_password):
                    if check_password_hash(info["password"], new_password):
                        error = "You've entered your previous password"
                    elif " " in  new_password:
                        error = "Please don't enter whitespaces in your new password"
                    else:
                        db.execute(
                            'UPDATE user SET password = ? WHERE id = ?',
                            (generate_password_hash(new_password), info["id"])
                        )
                else:
                    error = "You've entered your current password incorrectly"
            else:
                error = "Please enter your current password to change your password"

        if not new_height and not new_weight and not new_password and new_location == info["user_location"]:
            error = "No settings have been changed"

        if error is not None:
            flash(error, "error")
        else:
            message = "You've successfully changed your settings!"
            flash(message, "success")
            db.commit()
            return redirect(url_for('user.user_settings'))

    return render_template('user/user_settings.html',
                           name=info["name"], weight=info["weight"], height=info["height"], email=info["email"],
                           password=info["password"], user_location=info["user_location"], bmi_statement=info["bmi_statement"],
                           calories_statement=info["calories_statement"], number_of_days=info["number_of_days"],
                           user_average_calories=info["user_average_calories"], food_exists=info["food_exists"],
                           snack_message=info["snack_message"], average_breakfast_calories=info["average_breakfast_calories"],
                           average_lunch_calories=info["average_lunch_calories"], average_dinner_calories=info["average_dinner_calories"],
                           average_snack_calories=info["average_snack_calories"])


@bp.route('/faq', methods=('GET', 'POST'))
@login_required
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
                return render_template('user/faq.html', queries=queries)
            # for row in queries:
<<<<<<< HEAD
<<<<<<< HEAD

#         if request.form['action'] == 'Answer':
#             qns = db.execute('SELECT question FROM question_and_answer WHERE id = ?', str(id)).fetchone()
#             return render_template('user/answer_faq.html', qns=qns)
#         if request.form['action'] == 'Delete':
#             db.execute('DELETE FROM question_and_answer WHERE id = ?', str(id)).fetchone()
#             return render_template('user/faq.html')

=======
=======
>>>>>>> 0eedb4bab939e6f3412bb08790160fb6a0b68c48
        if request.form['action'] == 'Answer':
            qns = db.execute('SELECT question FROM question_and_answer WHERE id = ?', str(id)).fetchone()
            return render_template('user/answer_faq.html', qns=qns)
        if request.form['action'] == 'Delete':
            db.execute('DELETE FROM question_and_answer WHERE id = ?', str(id)).fetchone()
            return render_template('user/faq.html')
<<<<<<< HEAD
>>>>>>> 0eedb4bab939e6f3412bb08790160fb6a0b68c48
=======
>>>>>>> 0eedb4bab939e6f3412bb08790160fb6a0b68c48
        elif request.method == 'GET':
            if request.form['answer'] == 'Answer':
                qns = db.execute('SELECT question FROM question_and_answer WHERE id = ?', id).fetchone()
                return render_template('user/answer_faq.html', qns=qns)
            elif request.form['delete'] == 'Delete':
                db.execute('DELETE FROM question_and_answer WHERE id = ?', id).fetchone()
                return render_template('user/faq.html')
<<<<<<< HEAD
<<<<<<< HEAD

=======
>>>>>>> 0eedb4bab939e6f3412bb08790160fb6a0b68c48
    queries = db.execute('SELECT id, question, answer FROM question_and_answer').fetchall()
    # queries = list(map(lambda x: x[0], queries))
    # for row in queries:
    return render_template('user/faq.html', queries=queries)


# queries = list(map(lambda x: x[0], queries))


@bp.route('/answer/<int:id>', methods=('GET', 'POST'))
@login_required
def answer(id):
    db = get_db()
    qns = db.execute('SELECT question FROM question_and_answer WHERE id = ?', [id]).fetchone()
    if request.method == 'POST':
        if request.form['action'] == 'Submit Answer':
            answer = request.form['answer']
            if answer is None or answer == '':
                print(request.form)
                error = 'No value entered please try again'
                flash(error)
            else:
                db.execute('UPDATE question_and_answer SET answer= ? WHERE id = ?', (answer, id))
                db.commit()
                queries = db.execute('SELECT id, question, answer FROM question_and_answer').fetchall()
                return render_template('user/faq.html', queries=queries)
    return render_template('user/answer_faq.html', id=id, qns=qns[0])


