from werkzeug.security import check_password_hash, generate_password_hash
from foodhubsg.vendors import *
import sqlite3

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

    for user in users:
        id = user['id']
        name = user['name']
        weight = user['weight']
        height = user['height']
        email = user['email']
        user_location = user['location']
        password = user['password']

    bmi = round(weight / height ** height, 2)
    all_dates = []
    food_dates = []
    calories_list = []
    breakfast_list = []
    lunch_list = []
    dinner_list = []
    snack_list = []
    user_average_calories = 0
    number_of_days = 0
    average_breakfast_calories = 0
    average_lunch_calories = 0
    average_dinner_calories = 0
    average_snack_calories = 0
    calories_statement = None
    snack_message = None
    password_placeholder = "(unchanged)"

    if food_items == []:
        food_exists = 0
    else:
        food_exists = 1

    for food in food_items:
        food_date = food['created'].strftime('%d-%m-%y')
        all_dates.append(food_date)
    all_dates = remove_duplicates(all_dates)

    for date in all_dates:
        current_date_food = []
        current_date_calories = []

        for food in food_items:
            if date == food['created'].strftime('%d-%m-%y'):
                current_date_food.append(food)
                current_date_calories.append(food['calories'])
            else:
                continue

        food_dates.append(current_date_food)
        current_date_calories = sum(current_date_calories)
        calories_list.append(current_date_calories)

        number_of_days = len(calories_list)

        user_average_calories = int(sum(calories_list)/number_of_days)

    for food in food_items:
        if 5 <= int(food['created'].strftime('%H')) <= 9:
            breakfast_list.append(food['calories'])
            average_breakfast_calories = round(sum(breakfast_list) / number_of_days, 2)
        elif 11 <= int(food['created'].strftime('%H')) <= 14:
            lunch_list.append(food['calories'])
            average_lunch_calories = round(sum(lunch_list) / number_of_days, 2)
        elif 17 <= int(food['created'].strftime('%H')) <= 21:
            dinner_list.append(food['calories'])
            average_dinner_calories = round(sum(dinner_list) / number_of_days, 2)
        else:
            snack_list.append(food['calories'])
            average_snack_calories = round(sum(snack_list) / number_of_days, 2)

    ideal_weight = weight

    if bmi < 22:
        while ideal_weight / height ** height < 23:
            ideal_weight = ideal_weight + 1
        lose_weight = ideal_weight - weight
        bmi_statement = "{0}, you have a BMI of {1}, which is below the healthy range of 22 to 24. You are recommended " \
                        "to gain {2} kg to reach a body mass of {3} kg, which will get you back to the healthy BMI range." \
                        .format(name, bmi, lose_weight, ideal_weight)
    elif 22 < bmi < 24:
        bmi_statement = "{0}, you have a BMI of {1}, which is exactly within the healthy BMI range. " \
                        "Keep it up!".format(name, bmi)

    elif bmi > 24:
        while ideal_weight / height ** height > 23:
            ideal_weight = ideal_weight - 1
        lose_weight = weight - ideal_weight
        bmi_statement = "{0}, you have a BMI of {1}, which is above the healthy range of 22 to 24. You are recommended " \
                        "to lose {2} kg to reach a body mass of {3} kg, which will get you back to the healthy BMI range." \
                        .format(name, bmi, lose_weight, ideal_weight)

    if user_average_calories:
        if user_average_calories < 1500:
            calories_statement = "You consumed an average of {0} kcal daily over the last {1} days you've entered food " \
                                 "into your food journal, which is below the daily recommended amount of 2500 kcal."\
                                .format(user_average_calories, number_of_days)
        elif 1500 <= user_average_calories <= 2500:
            calories_statement = "You consumed an average of {0} kcal daily over the {1} days you've entered food " \
                                 "into your food journal, which is within the daily recommended amount, so keep following your current diet." \
                                .format(user_average_calories, number_of_days)

        elif user_average_calories > 2500:
            calories_statement = "You consumed an average of {} kcal daily over the last {} days you've entered food " \
                                 "which is above the daily recommended amount of 2500 kcal." \
                                .format(user_average_calories, number_of_days)

    if average_snack_calories:
        if average_snack_calories > 300:
            snack_message = "Also, you need to decrease your out-of-schedule snack intake."

    if request.method == 'POST':
        new_height = request.form['height']
        new_weight = request.form['weight']
        new_password = request.form['password']
        new_location = request.form.get('new-location')
        old_password = request.form['old-password']
        error = None
        message = None

        try:
            if new_height:
                if not 0.5 < float(new_height) < 2.5:
                    error = 'Please enter a valid height value in meters'
                elif new_height == height:
                    error = 'Please enter a new height value'
                else:
                    db.execute(
                        'UPDATE user SET height = ? WHERE id = ?',
                        (new_height, id)
                    )

            if new_weight:
                if not 20 < float(new_weight) < 250:
                    error = 'Please enter a valid weight value in kilograms'
                elif new_weight == weight:
                    error = 'Please enter a new weight value'
                else:
                    db.execute(
                        'UPDATE user SET weight = ? WHERE id = ?',
                        (new_weight, id)
                    )

            if new_location:
                db.execute(
                    'UPDATE user SET location = ? WHERE id = ?',
                    (new_location, id)
                )
            else:
                error = "Previous location selected"

            if new_password:
                if old_password:
                    if check_password_hash(password, old_password):
                        if check_password_hash(password, new_password):
                            error = "You've entered your previous password"
                        elif " " in  new_password:
                            error = "Please don't enter whitespaces in your new password"
                        else:
                            db.execute(
                                'UPDATE user SET password = ? WHERE id = ?',
                                (generate_password_hash(new_password), id)
                            )
                            password_placeholder = "(changed)"
                    else:
                        error = "You've entered your current password incorrectly"
                else:
                    error = "Please enter your current password to change your password"

            if not new_height and not new_weight and not new_password and new_location == user_location:
                error = "No settings have been changed"

        except ValueError:
            error = "Please enter a valid value"

        if error is not None:
            flash(error, "error")
        else:
            message = "You've successfully changed your settings!"
            flash(message, "success")
            db.commit()
            return redirect(url_for('user.user_settings'))

    return render_template('user/user_settings.html',
                           name=name, weight=weight, height=height, email=email, password=password, user_location=user_location, bmi_statement=bmi_statement,
                           calories_statement=calories_statement, number_of_days=number_of_days, user_average_calories=user_average_calories,
                           food_exists=food_exists, password_placeholder=password_placeholder, snack_message=snack_message,
                           average_breakfast_calories=average_breakfast_calories, average_lunch_calories=average_lunch_calories,
                           average_dinner_calories=average_dinner_calories, average_snack_calories=average_snack_calories)


@bp.route('/faq', methods=('GET', 'POST'))
@login_required
def faq():
    db = get_db()
    if request.method == 'POST':
        error = None
        if request.form['action'] == 'Submit A Question':
            question = request.form['query']
            answer = "No answer given yet, please answer on your own"
            if question is None:
                error = 'No value entered please try again'
            if error is None:
                db.execute('INSERT INTO question_and_answer (question, answer) VALUES (?, ?)', (question, answer))
                db.commit()
                queries = db.execute('SELECT id, question FROM question_and_answer').fetchall()
                return render_template('user/faq.html', queries=queries)
            # for row in queries:
            else:
                flash(error)
        elif request.method == 'GET':
            if request.form['answer'] == 'Answer':
                question_no= request.args.get("question_no", id)
                qns = db.execute('SELECT question FROM question_and_answer WHERE id = ?', id).fetchone()
                return render_template('user/answon Whereer_faq.html', qns=qns)
            elif request.form['user'] == 'Delete':
                return render_template('user/faq.html')
    queries = db.execute('SELECT id, question FROM question_and_answer').fetchall()
    # queries = list(map(lambda x: x[0], queries))
    # for row in queries:
    return render_template('user/faq.html', queries=queries)


# queries = list(map(lambda x: x[0], queries))


@bp.route('/answer/<int:id>', methods=('GET', 'POST'))
@login_required
def answer(id):
    if request.method == 'POST':
        db = get_db()
        qns = db.execute('SELECT question FROM question_and_answer WHERE id = ?', [id]).fetchone()
        if request.form['action'] == 'Submit Answer':
            if request.method == 'POST':
                print(request.form)
                answer = request.form['answer']

                abort(404, "Error")

        return render_template('user/answer_faq.html', id=id, qns=qns[0])


