# /your_project/api/resources/decryption_resource.py
from cryptography.fernet import Fernet

from .base_resource import BaseResource
from .. import api_blueprint


@api_blueprint.route('/decrypt')
class DecryptionResource(BaseResource):
    def post(self):
        args = self.parse_args()
        decrypted_text = self.process_text(args['text'], args['token'], Fernet.decrypt)
        return {"decrypted_text": decrypted_text}, 200
