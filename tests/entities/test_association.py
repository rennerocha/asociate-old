import uuid
import pytest

from asociate.entities.association import Association, Membership


def test_association_init():
    code = uuid.uuid4()

    association = Association(
        code=code, name="Association Name", slug="association_name"
    )

    assert association.code == str(code)
    assert association.name == "Association Name"
    assert association.slug == "association_name"


def test_association_str():
    code = uuid.uuid4()
    association = Association(
        code=code, name="Association Name", slug="association_name"
    )

    assert str(association) == f"<Association: {association.name}>"


def test_association_init_from_dict():
    code = uuid.uuid4()

    association_dict = {
        "code": code,
        "name": "Association Name",
        "slug": "association_name",
    }
    association = Association.from_dict(association_dict)

    assert association.name == "Association Name"


def test_association_add_new_member(association, member):
    association.add_as_member(member)

    assert member in association.members


def test_association_add_member_only_once(association, member):
    association.add_as_member(member)
    association.add_as_member(member)

    assert association.members.count(member) == 1


def test_error_if_try_add_not_valid_member(association):
    with pytest.raises(ValueError) as excinfo:
        association.add_as_member("not_a_member_instance")

    assert "Expected Member instance." in str(excinfo.value)


def test_association_add_new_member_create_new_membership(association, member):
    association.add_as_member(member)
    assert len(association.memberships) == 1

    membership = association.memberships.pop()

    assert isinstance(membership, Membership)
    assert membership.association == association
    assert membership.member == member
