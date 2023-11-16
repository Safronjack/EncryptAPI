# /your_project/main.py
from flask import Flask
from flask_restful import Api


flask_app = Flask(__name__)

api = Api(flask_app)

if __name__ == '__main__':
    flask_app.run(debug=True)
