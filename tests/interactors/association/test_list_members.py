from asociate.interactors.association import AssociationListMembers
from asociate.repository.exceptions import AssociationNotFoundError


def test_association_list_all_members(mocker, association_with_members):
    association_members = association_with_members.members

    repo = mocker.Mock()
    repo.list_members.return_value = association_members

    uc = AssociationListMembers(repo)
    response = uc.execute(association_code=association_with_members.code)
    assert bool(response) is True

    repo.list_members.assert_called_with(association_with_members.code)

    assert response.value == association_members


def test_list_members_handles_generic_error(mocker):
    repo = mocker.Mock()
    repo.list_members.side_effect = Exception('Just an error message')

    uc = AssociationListMembers(repo)
    response = uc.execute(association_code="any_code")
    
    assert bool(response) is False
    assert response.value == {
        "error": True,
        "type": "Exception",
        "message": "Just an error message"
    }


def test_error_when_list_member_of_inexistent_association(mocker):
    invalid_association_code = "invalid_association_code"

    repo = mocker.Mock()
    repo.list_members.side_effect = AssociationNotFoundError(f"Unable to find association with code {invalid_association_code}")

    uc = AssociationListMembers(repo)
    response = uc.execute(association_code=invalid_association_code)
    
    repo.list_members.assert_called_with(invalid_association_code)
    assert bool(response) is False
    assert response.value == {
        "error": True,
        "type": "AssociationNotFoundError",
        "message": f"Unable to find association with code {invalid_association_code}"
    }