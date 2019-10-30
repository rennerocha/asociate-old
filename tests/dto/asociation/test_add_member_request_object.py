import pytest

from asociate.dto.association import AddMemberRequestObject

pytestmark = [
    pytest.mark.dto,
]


# def test_add_member_request_comparison():
#     request_1 = AddMemberRequestObject.from_dict(
#         {"association_code": "A Code", "member": {"adict": ""}}
#     )
#     request_2 = AddMemberRequestObject.from_dict(
#         {"association_code": "A Code", "member": {"adict": ""}}
#     )
#     assert request_1 == request_2

#     request_3 = AddMemberRequestObject.from_dict(
#         {"association_code": "A Code", "member": {"anotherdict": ""}}
#     )
#     assert request_1 != request_3


def test_build_add_member_request_object_from_dict_invalid_param():
    request = AddMemberRequestObject.from_dict({"invalid_param": "invalid_param"})

    assert bool(request) is False
    assert request.has_errors()
    assert len(request.errors) == 3

    expected_errors = [
        {"parameter": "invalid_param", "message": "Unexpected parameter"},
        {"parameter": "association_code", "message": "Required"},
        {"parameter": "member", "message": "Required"},
    ]
    for error in request.errors:
        assert error in expected_errors


def test_build_add_member_request_object_from_dict_valid_param():
    request = AddMemberRequestObject.from_dict(
        {"association_code": "a code", "member": {}}
    )
    assert bool(request) is True

    assert request.association_code == "a code"
    assert request.member == {}
