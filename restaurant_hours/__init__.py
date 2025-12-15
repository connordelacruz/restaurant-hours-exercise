import os

from flask import Flask

from . import constants
from . import db
from . import csv_parser
from . import hours_checker
from . import api


def create_app(test_config=None):
    '''Create flask app.'''
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'restaurant_hours.db'),
    )

    if test_config is None:
        # Load the instance config (if it exists) when not testing.
        app.config.from_pyfile('config.py', silent=True)
    else:
        # Load the test config (if provided).
        app.config.from_mapping(test_config)

    # Make sure instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # Initialize database
    db.init_app(app)
    # Initialize API
    api.init_app(app)

    return app