# /your_project/api/resources/encryption_resource.py
from cryptography.fernet import Fernet
from .base_resource import BaseResource
from .. import api_blueprint


@api_blueprint.route('/encrypt')
class EncryptionResource(BaseResource):
    """
        Resource for encrypting text.

        Route: /encrypt
        Methods: POST
        """
    def post(self):
        """
                Handle the POST request for encrypting text.

                Returns:
                    dict: Encrypted text and HTTP status code.
                """
        args = self.parse_args()
        encrypted_text = self.process_text(args['text'], args['token'], Fernet.encrypt)
        return {"encrypted_text": encrypted_text}, 200
