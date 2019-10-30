import pytest

from asociate.dto.association import AddMemberRequestObject
from asociate.interactors.association import AssociationAddMember
from asociate.repository.exceptions import (
    AssociationNotFoundError,
    InvalidMemberDataError,
)

pytestmark = [
    pytest.mark.interactors,
]


def test_association_add_a_member(mocker, association, member):
    repo = mocker.Mock()

    uc = AssociationAddMember(repo)

    member_data = member.to_dict()
    request = AddMemberRequestObject(
        association_code=association.code, member=member_data,
    )
    response = uc.execute(request)
    assert bool(response) is True

    repo.add_member.assert_called_with(association.code, member_data)


def test_association_add_a_member_invalid_association(mocker, member):
    invalid_association_code = "invalid_code"
    repo = mocker.Mock()
    repo.add_member.side_effect = AssociationNotFoundError(
        f"Unable to find association with code {invalid_association_code}"
    )

    uc = AssociationAddMember(repo)

    member_data = member.to_dict()
    request = AddMemberRequestObject(
        association_code=invalid_association_code, member=member_data,
    )
    response = uc.execute(request)
    assert bool(response) is False

    repo.add_member.assert_called_with(invalid_association_code, member_data)
    assert response.value == {
        "error": True,
        "type": "AssociationNotFoundError",
        "message": f"Unable to find association with code {invalid_association_code}",
    }


def test_association_add_member_with_all_required_fields_missing(mocker):
    repo = mocker.Mock()
    repo.add_member.side_effect = InvalidMemberDataError(
        "Invalid member data provided."
    )

    member_data = {}
    uc = AssociationAddMember(repo)

    request = AddMemberRequestObject(
        association_code="association_code", member=member_data,
    )
    response = uc.execute(request)
    assert bool(response) is False

    assert response.value == {
        "error": True,
        "type": "InvalidMemberDataError",
        "message": "Invalid member data provided.",
    }


def test_association_add_a_member_with_all_required_fields(mocker, member):
    repo = mocker.Mock()
    repo.add_member.return_value = member

    uc = AssociationAddMember(repo)

    request = AddMemberRequestObject(
        association_code="association_code", member=member.to_dict(),
    )
    response = uc.execute(request)
    assert bool(response) is True

    assert repo.add_member.called
    assert response.value == member
