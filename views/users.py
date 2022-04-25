from flask import request
from flask_restx import Resource, Namespace, abort

from dao.model.user import UserSchema
from implemented import auth_service, user_service

users_ns = Namespace('users')


@users_ns.route('/<int:rid>')
class UserView(Resource):

    @auth_service.auth_required()
    def get(self, bid):
        user = user_service.get_one(bid)
        return UserSchema().dump(user), 200

    @auth_service.auth_required()
    def patch(self, bid):
        req_json = request.json

        if "id" not in req_json:
            req_json["id"] = bid
        user_service.update(req_json)

        return '', 204


@users_ns.route('/password/<int:rid>')
class UserPasswordView(Resource):

    @auth_service.auth_required()
    def put(self, bid):
        req_json = request.json

        password_1 = req_json.get('password_1')
        password_2 = req_json.get('password_2')

        user = user_service.get_one(bid)
        if not user:
            raise abort(404)

        checked_user = auth_service.check_user(user.username, password_1)
        if not checked_user:
            raise abort(400)

        user_service.update_password(user, password_2)

        return '', 204
