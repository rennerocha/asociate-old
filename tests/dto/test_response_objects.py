import pytest
from asociate.dto.response import ResponseFailure, ResponseSuccess


@pytest.fixture
def response_value():
    return {"key": ["value1", "value2"]}


def test_response_success_is_true():
    assert bool(ResponseSuccess()) is True


def test_response_success_has_type_and_value(response_value):
    response = ResponseSuccess(response_value)
    assert response.value == response_value


def test_response_failure_is_false():
    assert bool(ResponseFailure("")) is False


def test_response_failure_has_type_message_and_error():
    response = ResponseFailure(Exception("Just a failure"))

    assert response.value["error"] is True
    assert response.value["type"] == "Exception"
    assert response.value["message"] == "Just a failure"
