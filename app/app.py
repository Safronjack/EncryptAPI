# /your_project/app/app.py
from flask import Flask
from flask_restful import Api
import ssl


flask_app = Flask(__name__)

api = Api(flask_app)

from api import api_blueprint
from api.resources.token_resource import TokenResource
from api.resources.decryption_resource import DecryptionResource
from api.resources.encryption_resource import EncryptionResource

api.add_resource(TokenResource, '/token')
api.add_resource(EncryptionResource, '/encrypt')
api.add_resource(DecryptionResource, '/decrypt')


if __name__ == '__main__':
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    context.load_cert_chain(certfile='cert.pem', keyfile='key.pem')

    flask_app.run(debug=True, ssl_context=context)
