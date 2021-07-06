from werkzeug.exceptions import abort
from app.repository.post_db import Post
from app.repository.reaction_db import Reaction
from app.repository.database import db
from app.rbac import rbac
from datetime import datetime


def update_reaction(reaction_dict):
    user = rbac.get_current_user()
    if not user.username:
        abort(400, "No user logged in")
    post_id = reaction_dict["post_id"]
    like = reaction_dict["like"]
    post = Post.query.filter_by(id=post_id).first_or_404(
        f"Post with id {post_id} not found"
    )
    reaction = Reaction.query.filter_by(
        post_id=post_id, profile_username=user.username
    ).first()
    if not reaction:
        reaction = Reaction(profile_username=user.username)
    reaction.timestamp = datetime.now()
    reaction.like = like

    post.reactions.append(reaction)
    db.session.add(post)
    db.session.add(reaction)
    db.session.commit()
    return reaction
