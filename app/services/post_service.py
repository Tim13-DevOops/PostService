from datetime import datetime
from flask import abort
from app.repository.post_db import Post
from app.repository.database import db
from app.rbac import rbac
import logging
import json

logger = logging.getLogger(__name__)


def get_post_reactions_info(post):
    """Gets information about post reactions

    Returns:
        if the user liked the post,
        if the user disliked the post,
        number of likes,
        number of dislikes,
    """
    user = rbac.get_current_user()
    is_liked = any(
        reaction
        for reaction in post.reactions
        if reaction.profile_username == user.username and reaction.like
    )
    is_disliked = any(
        reaction
        for reaction in post.reactions
        if reaction.profile_username == user.username and not reaction.like
    )
    likes = len([reaction for reaction in post.reactions if reaction.like])
    dislikes = len([reaction for reaction in post.reactions if not reaction.like])
    return is_liked, is_disliked, likes, dislikes


def get_posts(page=1, page_size=10, filter_dict=None):
    page = int(page)
    page_size = int(page_size)

    if filter_dict is None:
        filter_dict = {}
    else:
        filter_dict = json.loads(filter_dict)
    filter_dict["deleted"] = False

    filters = []

    for k, v in filter_dict.items():
        if type(v) == str:
            filters.append(Post.__dict__[k].like(f"%{v}%"))
        else:
            filters.append(Post.__dict__[k] == v)

    query = (
        Post.query.filter(*filters)
        .order_by(Post.timestamp.desc())
        .paginate(page=page, per_page=page_size)
    )
    total = query.total  # noqa: F841
    posts = query.items
    for post in posts:
        liked_by_user, disliked_by_user, likes, dislikes = get_post_reactions_info(post)
        post.liked_by_user = liked_by_user
        post.disliked_by_user = disliked_by_user
        post.likes = likes
        post.dislikes = dislikes

    return posts


def get_post(post_id):
    post = Post.query.filter_by(id=post_id).first()
    if post is None:
        abort(404, f"Post with id {post_id} dost not exist")
    liked_by_user, disliked_by_user, likes, dislikes = get_post_reactions_info(post)
    post.liked_by_user = liked_by_user
    post.disliked_by_user = disliked_by_user
    post.likes = likes
    post.dislikes = dislikes
    return post


def create_post(post_dict):
    post_dict.pop("liked_by_user", None)
    post_dict.pop("disliked_by_user", None)
    post_dict.pop("likes", None)
    post_dict.pop("dislikes", None)
    user = rbac.get_current_user()
    post_dict["profile_username"] = user.username
    post_dict.pop("id", None)
    post = Post(**post_dict)
    post.timestamp = datetime.now()
    db.session.add(post)
    db.session.commit()
    return post


def delete_post(post_id):
    user = rbac.get_current_user()
    query = Post.query.filter_by(id=post_id)
    post = query.first()

    if post is None:
        abort(404, f"Invalid product id {post_id}")
    if post.agent_id != user.id:
        abort(404, "Product does not belog to this agent")

    query.update({"deleted": True})
    db.session.commit()
    return post
