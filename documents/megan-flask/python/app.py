from flask import *
from wtforms import BooleanField, StringField, PasswordField , validators
from werkzeug.security import check_password_hash, generate_password_hash
import sqlite3
from vendor_db import init_db, get_db
from stats import *
from user import *
from enter_code import *
app = Flask(__name__)
DATABASE = '../database/foodhub.db'
app.config.from_object(__name__)

with app.app_context():
    get_db()

def connect_to_database():
    return sqlite3.connect(app.config['DATABASE'])


codes = {}

@app.route('/homepage/<user>')
def homepage(user):
    init_db()
    connect_to_database()
    return render_template("homepage.html")


@app.route('/stats/<user>')
def stats(user):
    init_db()
    connect_to_database()
    return render_template("meal_journal.html", user=user)


@app.route('/<user>')
def profile(user):
    init_db()
    connect_to_database()
    userID = request.args.get("user", " ")
    return render_template("profile.html", user = userID)


@app.route('/enter')
def enter():
        init_db()
        connect_to_database()
        code = request.form("code")
        return render_template("enter_code.html")


if __name__ == '__main__':
    app.run(debug=True)
