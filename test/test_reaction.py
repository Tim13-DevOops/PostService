from app.app import app
from app.repository.database import db
from app.repository.post_db import Post
from app.repository.reaction_db import Reaction
import pytest
from datetime import datetime
from test.tokens import user1_token, user5_token
import json


def populate_db():

    post1 = Post(
        timestamp=datetime(2000, 5, 5, 5, 5, 5, 5),
        image="image1.jpg",
        description="description1",
        profile_username="user1panda",
    )

    post2 = Post(
        timestamp=datetime(2000, 5, 5, 5, 5, 5, 5),
        image="image2.jpg",
        description="description2",
        profile_username="user2panda",
    )

    post3 = Post(
        timestamp=datetime(2000, 5, 5, 5, 5, 5, 5),
        image="image3.jpg",
        description="description3",
        profile_username="user3panda",
    )

    post4 = Post(
        timestamp=datetime(2000, 5, 5, 5, 5, 5, 5),
        image="image4.jpg",
        description="description4",
        profile_username="user4panda",
    )

    reaction1 = Reaction(like=True, profile_username="user1panda")
    reaction2 = Reaction(like=True, profile_username="user2panda")
    reaction3 = Reaction(like=False, profile_username="user3panda")
    reaction4 = Reaction(like=True, profile_username="user1panda")
    reaction5 = Reaction(like=True, profile_username="user1panda")
    reaction6 = Reaction(like=False, profile_username="user1panda")
    post1.reactions.append(reaction1)
    post1.reactions.append(reaction2)
    post1.reactions.append(reaction3)
    post2.reactions.append(reaction4)
    post3.reactions.append(reaction5)
    post4.reactions.append(reaction6)

    db.session.add(reaction1)
    db.session.add(reaction2)
    db.session.add(reaction3)
    db.session.add(reaction4)
    db.session.add(reaction5)
    db.session.add(reaction6)
    db.session.add(post1)
    db.session.add(post2)
    db.session.add(post3)
    db.session.add(post4)
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


def test_get_liked_posts(client):
    # get posts for user user1panda
    result = client.get(
        "/post/like",
        headers={"Authorization": "Bearer " + user1_token},
    )
    assert len(result.json) == 3


def test_get_diliked_posts(client):
    # get posts for user user1panda
    result = client.get(
        "/post/dislike",
        headers={"Authorization": "Bearer " + user1_token},
    )
    assert len(result.json) == 1
