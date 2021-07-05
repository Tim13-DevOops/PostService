from app.app import app
from app.repository.database import db
import pytest

def populate_db():
    return

@pytest.fixture
def client():
    app.config["TESTING"] = True

    db.create_all()

    populate_db()

    with app.app_context():
        with app.test_client() as client:
            yield client

    db.session.remove()
    db.drop_all()


def test_hello(client):
    result = client.get("/")

    assert result.json["message"] == "Hello world"
