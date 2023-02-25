import base64
import hashlib
import hmac

from dao.user import UserDAO
from constants import PWD_HASH_SALT, PWD_HASH_ITERATIONS

class UserService:
    def __init__(self, dao: UserDAO):
        self.dao = dao

    def get_one(self, uid):
        return self.dao.get_one(uid)

    def get_all(self):
        return self.dao.get_all()

    def get_by_username(self, username):
        return self.dao.get_by_username(username)

    def create(self, user_data):
        user_data['password'] = self.make_user_password_hash(user_data.get('password'))
        return self.dao.create(user_data)

    def update(self, user_data):
        user_data['password'] = self.make_user_password_hash(user_data.get('password'))
        self.dao.update(user_data)
        return self.dao

    def delete(self, uid):
        self.dao.delete(uid)

    def make_user_password_hash(self, password):
        return base64.b64encode(hashlib.pbkdf2_hmac(
            'sha256',
            password.encode('utf-8'),
            PWD_HASH_SALT,
            PWD_HASH_ITERATIONS,
        ))

    def compare_passwords(self, password_hash, other_password):
        return hmac.compare_digest(
            password_hash,
            self.make_user_password_hash(other_password),
        )







