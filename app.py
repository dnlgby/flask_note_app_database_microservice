#  Copyright (c) 2023 Daniel Gabay

import os

from flask import Flask
from flask_injector import FlaskInjector
from injector import Injector, singleton
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists, create_database
from flask_smorest import Api
from dotenv import load_dotenv

from data.db import database
from di.module import UserRepositoryModule, UserServiceModule

from resources import UserBlueprint


def create_app():
    # Initialize the injector
    injector = Injector([UserRepositoryModule, UserServiceModule])
    app = Flask(__name__)
    FlaskInjector(app=app, injector=injector)

    # Load environment variables from existing '.env' files
    load_dotenv()

    # Flask
    app.config["PROPOGATE_EXCEPTION"] = True

    # API info
    app.config["API_TITLE"] = "Database service REST API"
    app.config["API_VERSION"] = "v1"

    # Open API
    app.config["OPENAPI_VERSION"] = "3.0.3"
    app.config["OPENAPI_URL_PREFIX"] = "/"
    app.config["OPENAPI_SWAGGER_UI_PATH"] = "/swagger-ui"
    app.config["OPENAPI_SWAGGER_UI_URL"] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"

    # Sqlalchemy
    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    if app.config["SQLALCHEMY_DATABASE_URI"] is None:
        raise ValueError("'DATABASE_URL' environment variable is not set")

    database.init_app(app)

    engine = create_engine(app.config["SQLALCHEMY_DATABASE_URI"])
    if not database_exists(engine.url):
        create_database(engine.url)

    # Database migration
    migrate = Migrate(app, database)

    # Flask-smorest extension wrapping
    api = Api(app)
    api.register_blueprint(UserBlueprint)

    # JWT - Will set on code for now for developing purposes
    app.config['JWT_SECRET_KEY'] = "255173194567594702208572596592176805026"
    jwt = JWTManager(app)

    # Initialize database tables before first request
    with app.app_context():
        database.create_all()

    return app
