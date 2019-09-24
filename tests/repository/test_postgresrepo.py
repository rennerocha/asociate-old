import pytest

from asociate.repository.exceptions import AssociationNotFoundError
from asociate.repository.postgresrepo import AssociationPostgresRepo


@pytest.mark.dbtest
def test_repository_list_without_parameters(
    docker_setup, pg_session, association_with_members
):
    repo = AssociationPostgresRepo(docker_setup["postgres"])
    members = repo.list_members(association_with_members.code)
    assert set(members) == set(association_with_members.members)


@pytest.mark.dbtest
def test_raises_error_when_try_list_association_that_does_not_exists(
    docker_setup, pg_session, association_with_members
):
    repo = AssociationPostgresRepo(docker_setup["postgres"])

    with pytest.raises(AssociationNotFoundError) as exc_info:
        members = repo.list_members("invalid_code")  # noqa

    assert exc_info.typename == "AssociationNotFoundError"
    assert exc_info.typename == "AssociationNotFoundError"
    assert exc_info.value == AssociationNotFoundError(
        "Unable to find association with code invalid_code"
    )
