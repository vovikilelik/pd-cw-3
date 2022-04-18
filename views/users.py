from flask import request
from flask_restx import Resource, Namespace

from implemented import auth_service, user_service

users_ns = Namespace('users')


@users_ns.route('/<int:rid>')
class UserView(Resource):

    @auth_service.auth_required('admin')
    def post(self):
        req_json = request.json
        user_service.create(req_json)
        return "", 201
