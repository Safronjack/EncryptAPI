# /your_project/app/__init__.py
from flask import Flask
from flask_restful import Api


def create_app():
    """
        Factory function for creating the Flask app and API.

        Returns:
            tuple: A tuple containing Flask app and Flask-RESTful API instances.
        """
    flask_app = Flask(__name__)

    api = Api(flask_app)

    from api import api_blueprint
    from api.resources.token_resource import TokenResource
    from api.resources.decryption_resource import DecryptionResource
    from api.resources.encryption_resource import EncryptionResource

    api.add_resource(TokenResource, '/token')
    api.add_resource(EncryptionResource, '/encrypt')
    api.add_resource(DecryptionResource, '/decrypt')

    return flask_app, api
