# Copyright (c) 2023 Daniel Gabay

import os

from dotenv import load_dotenv
from flask import Flask
from flask_injector import FlaskInjector
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from flask_smorest import Api
from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists, create_database

from app.data.db import database
from app.di.note_module import NoteModule
from app.di.user_module import UserModule
from app.resources import UserBlueprint, NoteBlueprint


def create_app(database_url=None):
    app = Flask(__name__)

    # Load environment variables from existing '.env' & '.flaskenv' files
    dotenv_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), '.env')
    load_dotenv(dotenv_path)

    flaskenv_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), '.flaskenv')
    load_dotenv(flaskenv_path)

    # Flask
    app.config["PROPOGATE_EXCEPTION"] = True

    # API info
    app.config["API_TITLE"] = "Database service REST API"
    app.config["API_VERSION"] = "v1"

    # Open API
    app.config["OPENAPI_VERSION"] = "3.0.0"
    app.config["OPENAPI_URL_PREFIX"] = "/"
    app.config["OPENAPI_SWAGGER_UI_PATH"] = "/swagger-ui"
    app.config["OPENAPI_SWAGGER_UI_URL"] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"

    # Flask-smorest documentation
    api = Api(app)
    api.register_blueprint(UserBlueprint)
    api.register_blueprint(NoteBlueprint)

    # ORM setup (SqlAlchemy)
    app.config["SQLALCHEMY_DATABASE_URI"] = database_url or os.getenv("DATABASE_URL")
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    if app.config["SQLALCHEMY_DATABASE_URI"] is None:
        raise ValueError("'DATABASE_URL' environment variable is not set")

    database.init_app(app)

    engine = create_engine(app.config["SQLALCHEMY_DATABASE_URI"])
    if not database_exists(engine.url):
        create_database(engine.url)

    # Database migration setup
    migrate = Migrate(app, database)

    # JWT - Will set on code for now for developing purposes
    secret_key = os.getenv('JWT_SECRET_KEY')
    if secret_key is None:
        raise ValueError("The JWT_SECRET_KEY environment variable must be set")

    app.config['JWT_SECRET_KEY'] = secret_key
    jwt = JWTManager(app)

    # Initialize database tables before first request
    with app.app_context():
        database.create_all()

    # Dependency injection
    FlaskInjector(app=app, modules=[UserModule, NoteModule])

    return app
