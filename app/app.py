# /your_project/app/app.py
from flask import Flask
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy

flask_app = Flask(__name__)
flask_app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///your_database.db'
flask_app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(flask_app)

api = Api(flask_app)

if __name__ == '__main__':
    db.create_all()
    flask_app.run(debug=True)
