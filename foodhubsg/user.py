from werkzeug.security import check_password_hash, generate_password_hash
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
        'SELECT id, name, email, password, height, weight'
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
    # breakfast_message = None
    # lunch_message = None
    # dinner_message = None
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
    #
    # if average_breakfast_calories:
    #     if average_breakfast_calories < 350:
    #         increase_breakfast = int(400 - average_breakfast_calories)
    #         breakfast_message = "increase your breakfast calorie intake by {} kcal against your current average of {} kcal " \
    #                             "to reach the ideal breakfast calorie amount of 400 kcal"\
    #                             .format(increase_breakfast, int(average_breakfast_calories))
    #     elif average_breakfast_calories > 500:
    #         decrease_breakfast = int(average_breakfast_calories - 400)
    #         breakfast_message = "decrease your breakfast calorie intake by {} kcal against your current average of {} kcal " \
    #                             "to reach the ideal breakfast calorie amount of 400 kcal"\
    #                             .format(decrease_breakfast, int(average_breakfast_calories))
    #
    # if average_lunch_calories:
    #     if average_lunch_calories < 650:
    #         increase_lunch = int(750 - average_lunch_calories)
    #         lunch_message = "increase your lunch calorie intake by {} kcal against your current average of {} kcal " \
    #                         "to reach the ideal lunch calorie amount of 650 kcal"\
    #                         .format(increase_lunch, int(average_lunch_calories))
    #     elif average_lunch_calories > 850:
    #         decrease_lunch =  int(average_lunch_calories - 750)
    #         lunch_message = "decrease your lunch calorie intake by {} kcal against your current average of {} kcal " \
    #                         "to reach the ideal lunch calorie amount of 650 kcal"\
    #                         .format(decrease_lunch, int(average_lunch_calories))
    #
    # if average_dinner_calories:
    #     if average_dinner_calories < 275:
    #         increase_dinner = int(300 - average_dinner_calories)
    #         dinner_message = "increase your dinner calorie intake by {} kcal against your current average of {} kcal " \
    #                         "to reach the ideal dinner calorie amount of 300 kcal"\
    #                         .format(increase_dinner, int(average_dinner_calories))
    #     elif average_dinner_calories > 350:
    #         decrease_dinner =  int(average_dinner_calories - 300)
    #         dinner_message = "decrease your dinner calorie intake by {} kcal against your current average of {} kcal " \
    #                         "to reach the ideal dinner calorie amount of 300 kcal"\
    #                         .format(decrease_dinner, int(average_dinner_calories))

    if average_snack_calories:
        if average_snack_calories > 300:
            snack_message = "Also, you need to decrease your out-of-schedule snack intake."

    # messages = [snack_message]
    # messages = list(filter(None.__ne__, messages))
    #
    # meal_message = "Also, you need to "
    # num_messages = len(messages)

    # if messages != []:
    #     for i in range(num_messages):
    #         if i != num_messages - 2 and i != num_messages - 1:
    #             meal_message += messages[i] + ", "
    #         elif i == num_messages - 2:
    #             meal_message += messages[i] + ", and "
    #         elif i == num_messages - 1:
    #             meal_message += messages[i] + "."
    # else:
    #     meal_message = None

    if request.method == 'POST':
        new_height = request.form['height']
        new_weight = request.form['weight']
        new_password = request.form['password']
        old_password = request.form['old-password']
        error = None
        message = None

        try:
            # if new_name:
            #     if not all(char.isalpha() or char.isspace() for char in new_name):
            #         error = 'Please only enter alphabets for your name'
            #     elif not len(new_name) < 16:
            #         error = 'Please enter a name below 16 characters'
            #     elif new_name.title() == name:
            #         error ='Please enter a new name'
            #     else:
            #         db.execute(
            #             'UPDATE user SET name = ? WHERE id = ?',
            #             (new_name.title(), id)
            #         )

            if not new_height and not new_weight and not new_password and not old_password:
                error = "No settings have been changed"

            elif old_password:

                if check_password_hash(password, old_password):

                    if new_height:
                        if not 0.5 < float(new_height) < 2.5:
                            error = 'Please enter a valid height value in meters'
                        elif new_height == height:
                            error ='Please enter a new height value'
                        else:
                            db.execute(
                                'UPDATE user SET height = ? WHERE id = ?',
                                (new_height, id)
                            )

                    if new_weight:
                        if not 20 < float(new_weight) < 250:
                            error = 'Please enter a valid weight value in kilograms'
                        elif new_weight == weight:
                            error ='Please enter a new weight value'
                        else:
                            db.execute(
                                'UPDATE user SET weight = ? WHERE id = ?',
                                (new_weight, id)
                            )

                    if new_password:
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

                    if not new_height and not new_weight and not new_password:
                        error = "No settings have been changed"

                else:
                    error = "You've entered your current password incorrectly"

            else:
                error = "Please enter your current password to confirm changes"

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
                           name=name, weight=weight, height=height, email=email, password=password, bmi_statement=bmi_statement,
                           calories_statement=calories_statement, number_of_days=number_of_days, user_average_calories=user_average_calories,
                           food_exists=food_exists, password_placeholder=password_placeholder, snack_message=snack_message,
                           average_breakfast_calories=average_breakfast_calories, average_lunch_calories=average_lunch_calories,
                           average_dinner_calories=average_dinner_calories, average_snack_calories=average_snack_calories)


@bp.route('/faq', methods=('GET', 'POST'))
@login_required
def faq():
    db = get_db()
    if request.method == 'POST':
        question = request.form['query']
        if request.form['action'] == 'submit-query':
            answer = "No answer given yet, please answer on your own"
            db.execute('INSERT INTO question_and_answer (question, answer) VALUES (?, ?)', (question, answer))
            db.commit()
            queries = db.execute('SELECT * FROM question_and_answer').fetchall()
            return render_template('user/faq.html', queries = queries)
        if request.form['action'] == 'answer-query':
            error = None
            return redirect(url_for('user.answer'))
    queries = db.execute('SELECT * FROM question_and_answer').fetchall()
    return render_template('user/faq.html', queries=queries)


@bp.route('/answer')
@login_required
def answer():
    return render_template('user/answer_faq.html')
    # db = get_db()
    #if request.method == 'POST':
        #answer = request.form['answer']
        #db.execute('INSERT INTO question_and_answer (answer) VALUES (?)', [answer])
        #db.commit()
        #return render_template('user/faq.html')

