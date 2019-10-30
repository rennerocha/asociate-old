import pytest

from asociate.repository.exceptions import AssociationNotFoundError
from asociate.repository.postgresrepo import AssociationPostgresRepo

pytestmark = [
    pytest.mark.dbtest,
]


def test_repository_list_without_parameters(
    docker_setup, pg_session, association_with_members
):
    repo = AssociationPostgresRepo(docker_setup["postgres"]["connection_string"])
    members = repo.list_members(association_with_members.code)
    assert set(members) == set(association_with_members.members)


def test_raises_error_when_try_list_association_that_does_not_exists(
    docker_setup, pg_session, association_with_members
):
    repo = AssociationPostgresRepo(docker_setup["postgres"]["connection_string"])

    with pytest.raises(AssociationNotFoundError) as exc_info:
        members = repo.list_members("invalid_code")  # noqa

    assert exc_info.typename == "AssociationNotFoundError"
    assert str(exc_info.value) == "Unable to find association with code invalid_code"


def test_repository_add_valid_member(docker_setup, pg_session, association, member):
    repo = AssociationPostgresRepo(docker_setup["postgres"]["connection_string"])
    repo.add_member(association.code, member.to_dict())

    assert member in repo.list_members(association.code)
