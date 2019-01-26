import os
from flask import Flask


app = Flask(__name__, instance_relative_config=True)
app.config.from_mapping(
    SECRET_KEY='this-is-totally-secret-guys-nobody-can-guess-this-trust-me',
    DATABASE=os.path.join(app.instance_path, 'foodhubsg.sqlite'),
)

try:
    os.makedirs(app.instance_path)
except OSError:
    pass

from foodhubsg import db
db.init_app(app)

from foodhubsg import auth, food, user, vendors, support
app.register_blueprint(auth.bp)
app.register_blueprint(food.bp)
app.register_blueprint(user.bp)
app.register_blueprint(vendors.bp)
app.register_blueprint(support.bp)

app.add_url_rule('/', endpoint='index')
