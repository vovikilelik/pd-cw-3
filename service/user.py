import base64
import hashlib
import hmac
from builtins import Exception

from constants import PWD_HASH_SALT, PWD_HASH_ITERATIONS, HASH_ALG
from dao.model.user import User
from dao.user import UserDAO


class UserService:
    def __init__(self, dao: UserDAO):
        self.dao = dao

    def create(self, username, password):
        return self.dao.create(User(username, self.get_hash(password)))

    def get_one(self, bid):
        return self.dao.get_one(bid)

    @staticmethod
    def get_hash(password):
        phash = hashlib.pbkdf2_hmac(
            HASH_ALG,
            password.encode('utf-8'),  # Convert the password to bytes
            PWD_HASH_SALT.encode(),
            PWD_HASH_ITERATIONS
        )

        return base64.b64encode(phash)

    def update(self, user_d, **overrides):
        return self.dao.update(user_d, overrides)

    def update_password(self, user_d, password):
        return self.dao.update(user_d, password=self.get_hash(password))

    def get_by_username(self, username):
        user = self.dao.search_one(username=username)
        return user

    def check_password(self, current_hash, sent):
        return current_hash == self.get_hash(sent)

    def check_user(self, username, password=None):
        user = self.get_by_username(username)
        return user if user and self.check_password(user.password, password) else None
