import calendar
import datetime
import hashlib

import jwt
from flask import request
from flask_restx import abort

from constants import PWD_HASH_SALT, PWD_HASH_ITERATIONS, HASH_ALG, JWT_SECRET, JWT_ALG
from service.user import UserService


def get_exp(length):
    timeout = datetime.datetime.utcnow() + datetime.timedelta(minutes=length)
    return calendar.timegm(timeout.timetuple())


class AuthService:
    def __init__(self, user_service: UserService):
        self.user_service = user_service

    def check_user(self, username, password):
        return self.user_service.check_user(username, password)

    @staticmethod
    def check_token(token):
        data = jwt.decode(token, JWT_SECRET, algorithms=JWT_ALG)

        if data['exp'] < calendar.timegm(datetime.datetime.utcnow().timetuple()):
            return False

        return data

    @staticmethod
    def generate_token(user):
        data = {
            'username': user.username
        }

        access_token = jwt.encode({**data, 'exp': get_exp(30)}, JWT_SECRET, algorithm=JWT_ALG)
        refresh_token = jwt.encode({**data, 'exp': get_exp(1000)}, JWT_SECRET, algorithm=JWT_ALG)

        return access_token, refresh_token

    @staticmethod
    def get_hash(password):
        return hashlib.pbkdf2_hmac(
            HASH_ALG,
            password.encode('utf-8'),
            PWD_HASH_SALT.encode(),
            PWD_HASH_ITERATIONS
        ).decode("utf-8", "ignore")

    @staticmethod
    def auth_required():
        def decorator_context(func):
            def wrapper(*args, **kwargs):
                req_json = request.json

                access_token = req_json.get('access_token')
                data = AuthService.check_token(access_token)

                if not data:
                    raise abort(403)

                return func(*args, **kwargs)

            return wrapper

        return decorator_context

