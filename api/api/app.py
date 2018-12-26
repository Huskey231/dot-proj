"""Flask application for dotProj API

"""
import os

from flask import Flask

from api import build


def create_app(config=None):
    """
    Flask Application factory
    :param config: Overriding config to use
    :return:
    """
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev'
    )

    if config is None:  # pragma no cover
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    app.register_blueprint(build.BLUEPIRNT, endpoint='build')
    return app
