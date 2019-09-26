import pytest
from unittest import mock
from asociate.dto.association import ListMembersRequestObject
from asociate.dto.response import ResponseFailure, ResponseSuccess
from asociate.repository.exceptions import AssociationNotFoundError


@mock.patch("asociate.web.association.AssociationListMembers")
@mock.patch("asociate.web.association.AssociationPostgresRepo")
def test_list_members_of_association_without_members(
    mock_repo, mock_interactor, client, association
):
    mock_interactor().execute.return_value = ResponseSuccess(value=[])

    response = client.get(f"/association/{association.code}/members")

    assert response.status_code == 200
    assert b"This association has no members." in response.data


@mock.patch("asociate.web.association.AssociationListMembers")
@mock.patch("asociate.web.association.AssociationPostgresRepo")
def test_list_all_members_of_association(
    mock_repo, mock_interactor, client, association_with_members
):
    mock_interactor().execute.return_value = ResponseSuccess(
        value=association_with_members.members
    )

    response = client.get(f"/association/{association_with_members.code}/members")

    for member in association_with_members.members:
        assert member.full_name in str(response.data)


@mock.patch("asociate.web.association.AssociationListMembers")
@mock.patch("asociate.web.association.AssociationPostgresRepo")
def test_list_members_of_inexistent_association(
    mock_repo, mock_interactor, client, association_with_members
):
    invalid_code = "invalid_code"
    error_msg = f"Unable to find association with code {invalid_code}"

    mock_interactor().execute.return_value = ResponseFailure(
        failure=AssociationNotFoundError(error_msg)
    )

    response = client.get(f"/association/{invalid_code}/members")

    assert response.status_code == 404
    assert error_msg in str(response.data)


@mock.patch("asociate.web.association.AssociationListMembers")
@mock.patch("asociate.web.association.AssociationPostgresRepo")
def test_request_object_initialisation_and_use(
    mock_repo, mock_interactor, client, association
):
    mock_interactor().execute.return_value = ResponseSuccess(value=[])

    internal_request_object = mock.Mock()
    request_object_class = \
        'asociate.web.association.ListMembersRequestObject'
    with mock.patch(request_object_class) as mock_request_object:
        mock_request_object.from_dict.return_value = internal_request_object
        client.get(f"/association/{association.code}/members")

    mock_request_object.from_dict.assert_called_with(
        {'association_code': association.code}
    )
    mock_interactor().execute.assert_called_with(internal_request_object)
