import pytest

from app import create_app


@pytest.fixture()
def app(tmp_path):
    return create_app(
        {
            "TESTING": True,
            "SECRET_KEY": "test-key",
            "DATABASE": str(tmp_path / "test.sqlite3"),
            "ADMIN_USERNAME": "admin",
            "ADMIN_PASSWORD": "admin",
        }
    )


@pytest.fixture()
def client(app):
    return app.test_client()


@pytest.fixture()
def logged_in(client):
    client.post("/login", data={"username": "admin", "password": "admin"})
    return client

