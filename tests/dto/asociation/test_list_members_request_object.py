from asociate.dto.association import ListMembersRequestObject


def test_build_list_members_request_object_with_param():
    request = ListMembersRequestObject(association_code="some_code")
    assert bool(request) is True
    assert request.association_code == "some_code"


def test_build_list_members_request_object_from_dict():
    request = ListMembersRequestObject.from_dict({"association_code": "some_code"})

    assert bool(request) is True
    assert request.association_code == "some_code"


def test_build_list_members_request_object_from_dict_invalid_param():
    request = ListMembersRequestObject.from_dict({"invalid_param": "invalid_param"})

    assert bool(request) is False
    assert request.has_errors()
    assert len(request.errors) == 2

    expected_errors = [
        {"parameter": "invalid_param", "message": "Unexpected parameter"},
        {"parameter": "association_code", "message": "Required"},
    ]
    for error in request.errors:
        assert error in expected_errors
