# /your_project/api/resources/decryption_resource.py
from cryptography.fernet import Fernet
from .base_resource import BaseResource
from .. import api_blueprint


@api_blueprint.route('/decrypt')
class DecryptionResource(BaseResource):
    """
        Resource for decrypting text.

        Route: /decrypt
        Methods: POST
        """
    def post(self):
        """
                Handle the POST request for decrypting text.

                Returns:
                    dict: Decrypted text and HTTP status code.
                """
        args = self.parse_args()
        decrypted_text = self.process_text(args['text'], args['token'], Fernet.decrypt)
        return {"decrypted_text": decrypted_text}, 200
