import psycopg2
import sqlalchemy
import sqlalchemy_utils
import pytest

from asociate.repository.models import Association, Base, Member


def pg_is_responsive(ip, docker_setup):
    try:
        conn = psycopg2.connect(
            "host={} user={} password={} dbname={}".format(
                ip,
                docker_setup["postgres"]["user"],
                docker_setup["postgres"]["password"],
                "postgres",
            )
        )
        conn.close()
        return True
    except psycopg2.OperationalError as exp:
        return False


@pytest.fixture(scope="session")
def pg_engine(docker_ip, docker_services, docker_setup):
    docker_services.wait_until_responsive(
        timeout=30.0, pause=0.1, check=lambda: pg_is_responsive(docker_ip, docker_setup)
    )
    engine = sqlalchemy.create_engine(docker_setup["postgres"]["connection_string"])
    sqlalchemy_utils.create_database(engine.url)
    conn = engine.connect()
    yield engine
    conn.close()


@pytest.fixture(scope="session")
def pg_session_empty(pg_engine):
    Base.metadata.create_all(pg_engine)
    Base.metadata.bind = pg_engine
    DBSession = sqlalchemy.orm.sessionmaker(bind=pg_engine)
    session = DBSession()
    yield session
    session.close()


@pytest.fixture(scope="function")
def pg_session(pg_session_empty, association_with_members):
    new_association = Association(
        code=association_with_members.code,
        name=association_with_members.name,
        slug=association_with_members.slug,
    )
    for member in association_with_members.members:
        new_member = Member(
            first_name=member.first_name,
            last_name=member.last_name,
            email=member.email,
            phone=member.phone,
            active=member.active,
        )
        new_association.members.append(new_member)

    pg_session_empty.add(new_association)

    pg_session_empty.commit()

    yield pg_session_empty

    pg_session_empty.query(Member).delete()
    pg_session_empty.query(Association).delete()
