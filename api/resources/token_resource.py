# /your_project/api/resources/token_resource.py
from cryptography.fernet import Fernet
from .base_resource import BaseResource
from .. import api_blueprint


@api_blueprint.route('/token')
class TokenResource(BaseResource):
    """
        Resource for generating an encryption/decryption token.

        Route: /token
        Methods: GET
        """
    def get(self):
        """
                Handle the GET request for generating an encryption/decryption token.

                Returns:
                    dict: Token and HTTP status code.
                """
        token_key = Fernet.generate_key()
        cipher_suite = Fernet(token_key)
        return {'token': token_key.decode()}, 200
