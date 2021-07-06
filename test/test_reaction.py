from app.app import app
from app.repository.database import db
from app.repository.post_db import Post
from app.repository.reaction_db import Reaction
import pytest
from datetime import datetime
from test.tokens import user1_token, user5_token
import json


def populate_db():

    post = Post(
        timestamp=datetime(2000, 5, 5, 5, 5, 5, 5),
        image="image1.jpg",
        description="description1",
        profile_username="user1panda",
    )

    reaction1 = Reaction(like=True, profile_username="user1panda")
    reaction2 = Reaction(like=True, profile_username="user2panda")
    reaction3 = Reaction(like=False, profile_username="user3panda")
    post.reactions.append(reaction1)
    post.reactions.append(reaction2)
    post.reactions.append(reaction3)

    db.session.add(reaction1)
    db.session.add(reaction2)
    db.session.add(reaction3)
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


def test_create_new_like_happy(client):
    result = client.put(
        "/reaction",
        data=json.dumps({"post_id": 1, "like": True}),
        content_type="application/json",
        headers={"Authorization": "Bearer " + user5_token},
    )
    assert result.status_code == 200
    result_get = client.get(
        "/post/1", headers={"Authorization": "Bearer " + user5_token}
    )
    assert result_get.json["likes"] == 3
    assert result_get.json["dislikes"] == 1
    assert result_get.json["liked_by_user"]
    assert not result_get.json["disliked_by_user"]


def test_create_new_like_sad(client):
    # exclude user token
    result = client.put(
        "/reaction",
        data=json.dumps({"post_id": 1, "like": True}),
        content_type="application/json",
        # headers={"Authorization": "Bearer " + user5_token},
    )
    assert result.status_code == 400
    result_get = client.get("/post/1")
    assert result_get.json["likes"] == 2
    assert result_get.json["dislikes"] == 1
    assert not result_get.json["liked_by_user"]
    assert not result_get.json["disliked_by_user"]


def test_create_new_dislike_happy(client):
    result = client.put(
        "/reaction",
        data=json.dumps({"post_id": 1, "like": False}),
        content_type="application/json",
        headers={"Authorization": "Bearer " + user5_token},
    )
    assert result.status_code == 200
    result_get = client.get(
        "/post/1", headers={"Authorization": "Bearer " + user5_token}
    )
    assert result_get.json["likes"] == 2
    assert result_get.json["dislikes"] == 2
    assert not result_get.json["liked_by_user"]
    assert result_get.json["disliked_by_user"]


def test_change_like_to_dislike(client):
    # use user token 1
    result = client.put(
        "/reaction",
        data=json.dumps({"post_id": 1, "like": False}),
        content_type="application/json",
        headers={"Authorization": "Bearer " + user1_token},
    )
    assert result.status_code == 200
    result_get = client.get(
        "/post/1", headers={"Authorization": "Bearer " + user1_token}
    )
    assert result_get.json["likes"] == 1
    assert result_get.json["dislikes"] == 2
    assert not result_get.json["liked_by_user"]
    assert result_get.json["disliked_by_user"]
