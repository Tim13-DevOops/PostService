from flask_restful import Resource
from flask import jsonify, request
from app.services import reaction_service


class ReactionAPI(Resource):
    def put(self):
        reaction_dict = request.get_json()
        return jsonify(reaction_service.update_reaction(reaction_dict))
