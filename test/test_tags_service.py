from app.app import app
from app.repository.database import db
from app.repository.post_db import Post
from app.repository.tag_db import Tag
import pytest
from datetime import datetime


def populate_db():

    post1 = Post(
        timestamp=datetime(2000, 5, 5, 5, 5, 5, 5),
        image="image1.jpg",
        description="description1",
        profile_username="user1",
    )
    post2 = Post(
        timestamp=datetime(2000, 5, 5, 5, 5, 5, 5),
        image="image2.jpg",
        description="description2",
        profile_username="user1",
    )
    tag1 = Tag(text="food")
    tag2 = Tag(text="food")
    tag3 = Tag(text="wine")
    post1.tags.append(tag1)
    post2.tags.append(tag2)
    post2.tags.append(tag3)
    db.session.add(post1)
    db.session.add(post2)
    db.session.add(tag1)
    db.session.add(tag2)
    db.session.add(tag3)
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


def test_get_posts_by_tag_happy(client):
    result = client.get("/post/tag/food")
    assert result.status_code == 200
    assert len(result.json) == 2
    result = client.get("/post/tag/wine")
    assert result.status_code == 200
    assert len(result.json) == 1
