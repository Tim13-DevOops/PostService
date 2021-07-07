from app.app import app
from app.repository.database import db
from app.repository.post_db import Post
import pytest
from datetime import datetime
from test.tokens import user1_token
import json


def populate_db():

    post = Post(
        timestamp=datetime(2000, 5, 5, 5, 5, 5, 5),
        image="image1.jpg",
        description="description1",
        profile_username="user1",
    )
    db.session.add(post)

    post = Post(
        timestamp=datetime(2000, 5, 5, 5, 5, 5, 5),
        image="image2.jpg",
        description="description2",
        profile_username="user1",
    )
    db.session.add(post)

    post = Post(
        timestamp=datetime(2000, 5, 5, 5, 5, 5, 5),
        image="image3.jpg",
        description="description3",
        profile_username="user2",
    )
    db.session.add(post)

    post = Post(
        timestamp=datetime(2000, 5, 5, 5, 5, 5, 5),
        image="image4.jpg",
        description="description4",
        profile_username="user2",
    )
    db.session.add(post)

    post = Post(
        timestamp=datetime(2000, 5, 5, 5, 5, 5, 5),
        image="image1.jpg",
        description="description1",
        profile_username="user2",
    )
    db.session.add(post)
    db.session.commit()


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


def test_get_all_happy(client):
    params = {"filter_dict": json.dumps({"profile_username": "user2"})}
    result = client.get("/post", query_string=params)

    assert len(result.json) == 3


def test_get_all_sad(client):
    params = {"filtero_dict": json.dumps({"profile_username": "user2"})}
    result = client.get("/post", query_string=params)

    assert result.status_code == 500


def test_get_one_happy(client):
    result = client.get("/post/1")

    assert result.json["id"] == 1
    assert result.json["image"] == "image1.jpg"
    assert result.json["description"] == "description1"
    assert result.json["profile_username"] == "user1"
    assert result.json["timestamp"] is not None
    assert result.json["deleted"] is False


def test_get_one_sad(client):
    result = client.get("/post/420")
    assert result.status_code == 404


def test_post_happy(client):

    post_dict = {
        "image": "image6.jpg",
        "description": "description6",
    }
    result = client.post(
        "/post",
        data=json.dumps(post_dict),
        headers={"Authorization": "Bearer " + user1_token},
        content_type="application/json",
    )

    assert result.json["id"] == 6
    assert result.json["image"] == "image6.jpg"
    assert result.json["description"] == "description6"
    assert result.json["profile_username"] == "user1panda"
    assert result.json["timestamp"] is not None
    assert result.json["deleted"] is False


def test_post_with_tags_happy(client):

    post_dict = {
        "image": "image6.jpg",
        "description": "description6",
        "tags": ["food", "wine"],
    }
    result = client.post(
        "/post",
        data=json.dumps(post_dict),
        headers={"Authorization": "Bearer " + user1_token},
        content_type="application/json",
    )

    assert result.json["id"] == 6
    assert result.json["image"] == "image6.jpg"
    assert result.json["description"] == "description6"
    assert result.json["profile_username"] == "user1panda"
    assert result.json["timestamp"] is not None
    assert result.json["deleted"] is False
    assert len(result.json["tags"]) == 2


def test_post_sad(client):

    post_dict = {
        "image": 1,
        "description": "description6",
    }
    result = client.post(
        "/post", data=post_dict, headers={"Authorization": "Bearer " + user1_token}
    )
    assert result.status_code == 500
