from flask import Flask
from dynaconf import settings
from asociate.web import association


def create_app():
    app = Flask(__name__, static_folder="static")

    app.config.from_mapping(
        ENV=settings.ENV,
        TESTING=settings.TESTING,
        DEBUG=settings.DEBUG,
        DB_CONNECTION_DATA = {
            "user": settings.DB_USER,
            "password": settings.DB_PASSWORD,
            "host": settings.DB_HOST,
            "dbname": settings.DB_NAME,
        }
    )
    app.register_blueprint(association.blueprint)

    return app
