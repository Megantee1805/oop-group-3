import os

from flask import Flask, render_template
from .classes import Food, Vendor


def create_app(test_config=None):
    """Create and configure an instance of the Flask application."""
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'foodhubsg.sqlite'),
    )

    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.update(test_config)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    from foodhubsg import db
    db.init_app(app)

    # apply the blueprints to the app
    from foodhubsg import auth, food, vendors, user
    app.register_blueprint(auth.bp)
    app.register_blueprint(food.bp)
    app.register_blueprint(vendors.bp)
    app.register_blueprint(user.bp)

    app.add_url_rule('/', endpoint='index')

    return app
