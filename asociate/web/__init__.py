from flask import Flask
from dynaconf import settings
from asociate.web import association


class Config:
    ...

class ProdConfig(Config):
    ENV = 'production'
    DEBUG = False

    DB_CONNECTION_DATA = {
        "user": "",
        "password": "",
        "host": "",
        "dbname": "",
    }

class DevConfig(Config):
    ENV = 'development'
    DEBUG = True

    DB_CONNECTION_DATA = {
        "user": "jhxglkog",
        "password": "uX88WHevfQyB_oOiGkucijagLGK_coVe",
        "host": "motty.db.elephantsql.com:5432",
        "dbname": "jhxglkog",
    }

class TestConfig(Config):
    ENV = 'test'
    TESTING = True
    DEBUG = True

    DB_CONNECTION_DATA = {
        "user": "test_db_user",
        "password": "test_db_password",
        "host": "test_db_host",
        "dbname": "test_dbname",
    }

def create_app(config_object=DevConfig):
    app = Flask(__name__, static_folder="static")
    app.config.from_object(config_object)
    app.register_blueprint(association.blueprint)

    return app