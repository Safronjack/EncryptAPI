# /your_project/app/app.py
from flask import Flask
from flask_restful import Api
from app.resources.resources import TokenResource, EncryptionResource, DecryptionResource, LogResource

app = Flask(__name__)
api = Api(app)

api.add_resource(TokenResource, '/token')
api.add_resource(EncryptionResource, '/encrypt')
api.add_resource(DecryptionResource, '/decrypt')
api.add_resource(LogResource, '/log')

if __name__ == '__main__':
    app.run(debug=True)
