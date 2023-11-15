# /your_project/app/__init__.py
from flask import Flask
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy

flask_app = Flask(__name__)
flask_app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///your_database.db'
flask_app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(flask_app)

api = Api(flask_app)

from api import api_blueprint
from api.resources.token_resource import TokenResource
from api.resources.decryption_resource import DecryptionResource
from api.resources.encryption_resource import EncryptionResource
from api.resources.log_resource import LogResource

api.add_resource(TokenResource, '/token')
api.add_resource(EncryptionResource, '/encrypt')
api.add_resource(DecryptionResource, '/decrypt')
api.add_resource(LogResource, '/log')


def create_app():
    with flask_app.app_context():
        db.create_all()
    return flask_app
