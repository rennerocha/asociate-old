from flask import Flask
from dynaconf import settings
from asociate.web import association

from sqlalchemy import create_engine

def create_app():
    app = Flask(__name__, static_folder="static")

    connection_string = "postgresql+psycopg2://{}:{}@{}/{}".format(
        settings.DB_USER,
        settings.DB_PASSWORD,
        settings.DB_HOST,
        settings.DB_NAME,
    )
    # global engine
    app.engine = create_engine(connection_string)

    app.config.from_mapping(
        ENV=settings.ENV,
        TESTING=settings.TESTING,
        DEBUG=settings.DEBUG,
        DB_CONNECTION_STRING=connection_string
    )

    app.register_blueprint(association.blueprint)

    return app
