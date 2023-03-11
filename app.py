#  Copyright (c) 2023 Daniel Gabay

import os

from dotenv import load_dotenv
from flask import Flask
from flask_injector import FlaskInjector
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from flask_smorest import Api
from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists, create_database

from data.db import database
from data.repositories.user_repository import UserRepository
from services.user_service import UserService

from resources import UserBlueprint


def create_app():
    app = Flask(__name__)

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

    # Flask-smorest extension wrapping
    api = Api(app)
    api.register_blueprint(UserBlueprint)

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

    # JWT - Will set on code for now for developing purposes
    app.config['JWT_SECRET_KEY'] = "255173194567594702208572596592176805026"
    jwt = JWTManager(app)

    # Initialize database tables before first request
    with app.app_context():
        database.create_all()

    # Configure the application's dependency injection
    def configure(binder):
        binder.bind(UserRepository, UserRepository())
        binder.bind(UserService, UserService(UserRepository()))

    FlaskInjector(app=app, modules=[configure])



    return app
