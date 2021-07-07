from app.repository.post_db import Post
from app.repository.tag_db import Tag
from app.services.post_service import get_post_reactions_info


def get_posts_by_tag(tag):
    posts = Post.query.filter(Post.tags.any(Tag.text == tag)).all()
    for post in posts:
        liked_by_user, disliked_by_user, likes, dislikes = get_post_reactions_info(post)
        post.liked_by_user = liked_by_user
        post.disliked_by_user = disliked_by_user
        post.likes = likes
        post.dislikes = dislikes

    return posts
