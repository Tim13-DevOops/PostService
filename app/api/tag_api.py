from flask_restful import Resource
from flask import jsonify
from app.services import tag_service


class TagAPI(Resource):
    def get(self, tag):
        return jsonify(tag_service.get_posts_by_tag(tag))
