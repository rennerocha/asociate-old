import pytest

from asociate.entities.member import Member


def test_member_init():
    member = Member(
        first_name="Arthur",
        last_name="Dent",
        email="arthur.dent@deepthought.com",
        phone="912340042",
        active=False,
    )
    assert member.first_name == "Arthur"
    assert member.last_name == "Dent"
    assert member.email == "arthur.dent@deepthought.com"
    assert member.phone == "912340042"


def test_member_init_from_dict():
    member_dict = {
        "first_name": "Arthur",
        "last_name": "Dent",
        "email": "arthur.dent@deepthought.com",
        "phone": "912340042",
    }
    member = Member.from_dict(member_dict)

    assert member.first_name == "Arthur"
    assert member.last_name == "Dent"
    assert member.email == "arthur.dent@deepthought.com"
    assert member.phone == "912340042"
    assert not member.active


def test_member_full_name():
    member_dict = {
        "first_name": "Arthur",
        "last_name": "Dent",
        "email": "arthur.dent@deepthought.com",
        "phone": "912340042",
    }
    member = Member.from_dict(member_dict)

    assert member.full_name == "Arthur Dent"

def test_member_repr():
    member = Member(
        first_name="Arthur",
        last_name="Dent",
        email="arthur.dent@deepthought.com",
        phone="912340042",
        active=False,
    )
    assert repr(member) == f"<Member: {member.first_name} {member.last_name}>"


def test_member_join_association(association, member):
    member.join(association)

    assert member in association.members


def test_error_if_try_join_not_valid_association(member):
    with pytest.raises(ValueError) as excinfo:
        member.join("not_a_valid_association_instance")

    assert "Expected Association instance." in str(excinfo.value)


def test_member_model_to_dict():
    member_dict = {
        "first_name": "Arthur",
        "last_name": "Dent",
        "email": "arthur.dent@deepthought.com",
        "phone": "912340042",
        "active": False,
    }
    member = Member.from_dict(member_dict)

    assert member.to_dict() == member_dict


def test_member_comparison():
    member_dict = {
        "first_name": "Arthur",
        "last_name": "Dent",
        "email": "arthur.dent@deepthought.com",
        "phone": "912340042",
    }
    member_1 = Member.from_dict(member_dict)
    member_2 = Member.from_dict(member_dict)

    assert member_1 == member_2
