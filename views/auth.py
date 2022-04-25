from flask import request
from flask_restx import Resource, Namespace, abort

from implemented import user_service, auth_service

auth_ns = Namespace('auth')


@auth_ns.route('/register')
class AuthRegisterView(Resource):

    def post(self):
        req_json = request.json

        username = req_json.get('username')
        password = req_json.get('password')

        user = user_service.create(username, password)

        access_token, refresh_token = auth_service.generate_token(user)
        return {'access_token': access_token, 'refresh_token': refresh_token}, 201


@auth_ns.route('/login')
class AuthView(Resource):
    def post(self):
        req_json = request.json

        username = req_json.get('username')
        password = req_json.get('password')

        user = auth_service.check_user(username, password)

        if not user:
            raise abort(400)

        access_token, refresh_token = auth_service.generate_token(user)
        return {'access_token': access_token, 'refresh_token': refresh_token}, 201

    def put(self):
        req_json = request.json
        refresh_token = req_json.get('refresh_token')

        data = auth_service.check_token(refresh_token)
        if not data:
            raise abort(403)

        user = user_service.get_by_username(data['username'])
        if not user:
            raise abort(400)

        access_token, refresh_token = auth_service.generate_token(user)
        return {'access_token': access_token, 'refresh_token': refresh_token}, 201
