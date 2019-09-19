import pytest

from asociate.web import create_app, TestConfig


@pytest.fixture
def app():
    app = create_app(TestConfig)
    return app