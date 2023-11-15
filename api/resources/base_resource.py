# /your_project/api/resources/base_resource.py
from flask import abort
from flask_restful import Resource, reqparse
from cryptography.fernet import Fernet
from api.models.models import LogEntry
from app.app import db  # Импортируем db из приложения

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
            return result_text.decode()
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
