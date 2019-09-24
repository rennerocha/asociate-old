import psycopg2
import sqlalchemy
import sqlalchemy_utils
import pytest

from asociate.repository.models import Association, Base, Member

from asociate.web import DevConfig

connection_data = DevConfig.DB_CONNECTION_DATA

conn_str = "postgres://{}:{}@{}/{}".format(
    connection_data["user"],
    connection_data["password"],
    connection_data["host"],
    connection_data["dbname"],
)
engine = sqlalchemy.create_engine(conn_str)
conn = engine.connect()
Base.metadata.create_all(engine)
conn.close()
