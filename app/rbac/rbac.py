from flask import request
import bcrypt

# import config
from werkzeug.exceptions import Forbidden, Unauthorized
from flask_jwt_extended import JWTManager, create_access_token, decode_token

import datetime
import app.config as config
import dataclasses


jwt = None


class AppUser:
    def __init__(
        self,
        id,
        timestamp,
        username,
        user_role,
        name,
        surname,
        email,
        phone_number,
        website,
        banned,
        deleted,
        agent_request=None,
    ):
        self.id = id
        self.timestamp = timestamp
        self.username = username
        self.user_role = user_role
        self.name = name
        self.surname = surname
        self.email = email
        self.phone_number = phone_number
        self.website = website
        self.banned = banned
        self.deleted = deleted


def get_hashed_password(plain_text_password):
    return bcrypt.hashpw(plain_text_password.encode("utf-8"), bcrypt.gensalt()).decode(
        "utf-8"
    )


def check_password(plain_text_password, hashed_password):
    return bcrypt.checkpw(
        plain_text_password.encode("utf-8"), hashed_password.encode("utf-8")
    )


def setJWTManager(app):
    app.config["SECRET_KEY"] = config.SECRET_KEY
    jwt = JWTManager(app)  # noqa: F841


def get_token(user_obj):
    """Get token for given user.

    Args:
        user_obj: AppUser object.
    """
    expires = datetime.timedelta(days=2)
    access_token = create_access_token(
        identity=dataclasses.asdict(user_obj), expires_delta=expires
    )
    return access_token


def get_current_user():
    if request.headers.get("Authorization") is None:
        return AppUser(
            id=None,
            timestamp=None,
            username=None,
            user_role="guest",
            name=None,
            surname=None,
            email=None,
            phone_number=None,
            website=None,
            banned=None,
            deleted=None,
        )
    token = request.headers.get("Authorization")[7:]
    user_dict = decode_token(token)["sub"]
    user = AppUser(**user_dict)
    return user


class Allow:
    def __init__(self, roles):
        self.roles = roles

    def __call__(self, fn):
        user = get_current_user()
        if user.user_role == "guest":
            raise Unauthorized()
        if user.user_role not in self.roles:
            raise Forbidden()
        return fn
