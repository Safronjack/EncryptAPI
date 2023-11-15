# resources.py
from flask import abort, Blueprint
from flask_restful import Resource, reqparse
from cryptography.fernet import Fernet
from app import db
from app.models.models import LogEntry


api_blueprint = Blueprint('api', __name__)


class BaseResource(Resource):
    ERROR_TEXT_NOT_PROVIDED = "Text not provided."
    ERROR_TOKEN_NOT_PROVIDED = "Token not provided."

    def process_text(self, text, token, operation):
        if not text:
            self.abort_with_error(self.ERROR_TEXT_NOT_PROVIDED)

        if not token:
            self.abort_with_error(self.ERROR_TOKEN_NOT_PROVIDED)

        try:
            cipher_suite = Fernet(token)
            result_text = operation(cipher_suite, text.encode())
            return result_text
        except Exception as e:
            error_message = f"Internal Server Error: {str(e)}"
            self.log_error(error_message)
            self.abort_with_error(error_message, 500)

    def log_info(self, message):
        log_entry = LogEntry(message=message, level='INFO')
        db.session.add(log_entry)
        db.session.commit()

    def log_error(self, message):
        log_entry = LogEntry(message=message, level='ERROR')
        db.session.add(log_entry)
        db.session.commit()

    def abort_with_error(self, message, status_code=400):
        self.log_error(message)
        abort(status_code, {'message': message})

    def parse_args(self):
        try:
            parser = reqparse.RequestParser()
            parser.add_argument('text', type=str, required=True, help='Text is required.')
            parser.add_argument('token', type=str, required=True, help='Token is required.')
            return parser.parse_args()
        except Exception as e:
            self.abort_with_error(f"Error parsing arguments: {str(e)}", 400)


@api_blueprint.route('/token')
class TokenResource(BaseResource):
    def get(self):
        token_key = Fernet.generate_key()
        cipher_suite = Fernet(token_key)
        return {'token': token_key.decode()}, 200


@api_blueprint.route('/encrypt')
class EncryptionResource(BaseResource):
    def post(self):
        args = self.parse_args()
        encrypted_text = self.process_text(args['text'], args['token'], Fernet.encrypt)
        return {"encrypted_text": encrypted_text.decode()}, 200


@api_blueprint.route('/decrypt')
class DecryptionResource(BaseResource):
    def post(self):
        args = self.parse_args()
        decrypted_text = self.process_text(args['text'], args['token'], Fernet.decrypt)
        return {"decrypted_text": decrypted_text.decode()}, 200


@api_blueprint.route('/log')
class LogResource(BaseResource):
    def get(self):
        logs = LogEntry.query.all()
        return {'logs': [{'message': log.message, 'level': log.level} for log in logs]}, 200

    def delete(self):
        LogEntry.query.delete()
        db.session.commit()
        return {'message': 'Log cleared successfully'}, 200
