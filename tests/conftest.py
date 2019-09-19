import uuid
import tempfile
import os
import yaml
import pytest

from asociate.entities.association import Association
from asociate.entities.member import Member


@pytest.fixture
def association():
    code = uuid.uuid4()

    association_dict = {"code": code, "name": "Heart Of Gold", "slug": "heart_of_gold"}
    return Association.from_dict(association_dict)


@pytest.fixture
def member():
    member_dict = {
        "first_name": "Arthur",
        "last_name": "Dent",
        "email": "arthur.dent@deepthought.com",
        "phone": "912340042",
    }
    return Member.from_dict(member_dict)


@pytest.fixture
def members(member):
    other_member_dict = {
        "first_name": "Ford",
        "last_name": "Prefect",
        "email": "ford.prefect@deepthought.com",
        "phone": "912340042",
    }
    other_member = Member.from_dict(other_member_dict)

    return [member, other_member]


@pytest.fixture
def association_with_members(association, members):
    for member in members:
        association.add_as_member(member)
    return association


@pytest.fixture(scope="session")
def docker_setup(docker_ip):
    return {
        "postgres": {
            "dbname": "asociate_db",
            "user": "postgres",
            "password": "asociate_pass",
            "host": docker_ip,
        }
    }


@pytest.fixture(scope="session")
def docker_tmpfile():
    f = tempfile.mkstemp()
    yield f
    os.remove(f[1])


@pytest.fixture(scope="session")
def docker_compose_file(docker_tmpfile, docker_setup):
    content = {
        "version": "3.1",
        "services": {
            "postgresql": {
                "restart": "always",
                "image": "postgres",
                "ports": ["5432:5432"],
                "environment": [
                    "POSTGRES_PASSWORD={}".format(docker_setup["postgres"]["password"])
                ],
            }
        },
    }

    f = os.fdopen(docker_tmpfile[0], "w")
    f.write(yaml.dump(content))
    f.close()
    return docker_tmpfile[1]
