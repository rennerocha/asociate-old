import pytest

from asociate.dto.request import InvalidRequestObject, ValidRequestObject

pytestmark = [
    pytest.mark.dto,
]


def test_valid_request_object_is_true():
    assert bool(ValidRequestObject()) is True


def test_invalid_request_object_is_false():
    assert bool(InvalidRequestObject()) is False


def test_empty_invalid_request_has_no_errors():
    request = InvalidRequestObject()
    assert not request.has_errors()


def test_can_add_error_into_invalid_request_object():
    request = InvalidRequestObject()
    request.add_error(parameter="a_parameter", message="a message")
    request.add_error(parameter="another_parameter", message="another message")

    assert request.has_errors()
    assert len(request.errors) == 2

    assert "a_parameter" in request.errors[0]["parameter"]
    assert "a message" in request.errors[0]["message"]

    assert "another_parameter" in request.errors[1]["parameter"]
    assert "another message" in request.errors[1]["message"]
