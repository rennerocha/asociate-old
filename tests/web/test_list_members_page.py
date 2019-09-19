import pytest
from unittest import mock
from asociate.response_objects import ResponseFailure, ResponseSuccess
from asociate.repository.exceptions import AssociationNotFoundError


@mock.patch('asociate.web.association.AssociationListMembers')
@mock.patch('asociate.web.association.AssociationPostgresRepo')
def test_list_members_of_association_without_members(mock_repo, mock_interactor, client, association):
    mock_interactor().execute.return_value = ResponseSuccess(value=[])

    response = client.get(f"/association/{association.code}/members")

    mock_interactor().execute.assert_called_with(association.code)
    assert response.status_code == 200
    assert b'This association has no members.' in response.data


@mock.patch('asociate.web.association.AssociationListMembers')
@mock.patch('asociate.web.association.AssociationPostgresRepo')
def test_list_all_members_of_association(mock_repo, mock_interactor, client, association_with_members):
    mock_interactor().execute.return_value = ResponseSuccess(value=association_with_members.members)    

    response = client.get(f"/association/{association_with_members.code}/members")

    for member in association_with_members.members:
        assert member.full_name in str(response.data)


@mock.patch('asociate.web.association.AssociationListMembers')
@mock.patch('asociate.web.association.AssociationPostgresRepo')
def test_list_members_of_inexistent_association(mock_repo, mock_interactor, client, association_with_members):
    invalid_code = "invalid_code"

    mock_interactor().execute.return_value = ResponseFailure(
        failure=AssociationNotFoundError(
            f"Unable to find association with code {invalid_code}"
        )
    )    

    response = client.get(f"/association/{invalid_code}/members")