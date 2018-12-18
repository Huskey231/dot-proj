import pytest
from dot_proj_api import create_app


@pytest.fixture
def app():
    app = create_app({
        'TESTING': True
    })

    return app


@pytest.fixture
def client(app):
    return app.test_client()
