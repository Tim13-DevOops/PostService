from flask_restful import Resource
from flask import jsonify, request
from app.services import post_service
from app.rbac import rbac


class PostAPI(Resource):
    method_decorators = {
        "post": [rbac.Allow(["user", "agent"])],
    }

    def get(self):
        return jsonify(post_service.get_posts(**request.args))

    def post(self):
        product_dict = request.get_json()
        return jsonify(post_service.create_post(product_dict))


class SinglePostAPI(Resource):
    method_decorators = {
        "delete": [rbac.Allow(["user", "agent"])],
    }

    def get(self, post_id):
        return jsonify(post_service.get_post(post_id))

    def delete(self, post_id):
        return jsonify(post_service.delete_post(post_id))


class LikedPostAPI(Resource):
    def get(self):
        return jsonify(post_service.get_reacted_posts(True))


class DislikedPostAPI(Resource):
    def get(self):
        return jsonify(post_service.get_reacted_posts(False))
