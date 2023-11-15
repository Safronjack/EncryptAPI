# /your_project/api/resources/token_resource.py
from cryptography.fernet import Fernet
from .base_resource import BaseResource
from app.app import db
from api.models.log_entry import LogEntry
from .. import api_blueprint


@api_blueprint.route('/token')
class TokenResource(BaseResource):
    def get(self):
        token_key = Fernet.generate_key()
        cipher_suite = Fernet(token_key)
        return {'token': token_key.decode()}, 200
