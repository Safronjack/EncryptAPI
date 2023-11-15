# /your_project/app/__init__.py
from flask import Flask
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///your_database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

api = Api(app)

from api import api_blueprint  # Импортируем blueprint
from api.resources.token_resource import TokenResource
from api.resources.decryption_resource import DecryptionResource
from api.resources.encryption_resource import EncryptionResource
from api.resources.log_resource import LogResource


api.add_resource(TokenResource, '/token')
api.add_resource(EncryptionResource, '/encrypt')
api.add_resource(DecryptionResource, '/decrypt')
api.add_resource(LogResource, '/log')

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
