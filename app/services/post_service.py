from datetime import datetime
from flask import abort
from app.repository.post_db import Post
from app.repository.database import db
from app.rbac import rbac
import logging
import json

logger = logging.getLogger(__name__)

def get_posts(page=1, page_size=10, filter_dict="\{\}"):
    page = int(page)
    page_size = int(page_size)


    filter_dict = json.loads(filter_dict)
    filter_dict['deleted'] = False

    filters = []

    for k, v in filter_dict.items():
        if type(v) == str:
            filters.append(Post.__dict__[k].like(f"%{v}%"))
        else:
            filters.append(Post.__dict__[k] == v)

    
    query = Post.query.filter(*filters).order_by(Post.timestamp.desc()).paginate(page=page, per_page=page_size)
    total = query.total
    posts = query.items

    return posts

def get_post(post_id):
    post = Post.query.filter_by(id=post_id).first()
    if post == None:
        abort(404, f"Post with id {post_id} dost not exist")
    return post

def create_post(post_dict):
    user = rbac.get_current_user()
    post_dict['profile_username'] = user.username
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

    if post == None:
        abort(404, f"Invalid product id {post_id}")
    if post.agent_id != user.id:
        abort(404, "Product does not belog to this agent")

    query.update({"deleted": True})
    db.session.commit()
    return post

