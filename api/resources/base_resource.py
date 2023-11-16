# /your_project/api/resources/base_resource.py
from flask import abort
from flask_restful import Resource, reqparse
from cryptography.fernet import Fernet


class BaseResource(Resource):
    """
        Base class for API resources providing common functionality.

        Attributes:
            ERROR_TEXT_NOT_PROVIDED (str): Error message for missing text.
            ERROR_TOKEN_NOT_PROVIDED (str): Error message for missing token.
        """
    ERROR_TEXT_NOT_PROVIDED = "Text not provided."
    ERROR_TOKEN_NOT_PROVIDED = "Token not provided."

    def process_text(self, text, token, operation):
        """
                Process the provided text using the given operation and token.

                Args:
                    text (str): The text to process.
                    token (str): The encryption/decryption token.
                    operation (function): The encryption/decryption function.

                Returns:
                    str: The result of the operation.

                Raises:
                    HTTPException: If text or token is missing, or if an internal server error occurs.
                """
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
            self.abort_with_error(error_message, 500)

    def abort_with_error(self, message, status_code=400):
        """
                Abort the request with a custom error message and status code.

                Args:
                    message (str): The error message.
                    status_code (int): The HTTP status code.

                Raises:
                    HTTPException: With the specified error message and status code.
                """
        abort(status_code, {'message': message})

    def parse_args(self):
        """
                Parse and retrieve request arguments.

                Returns:
                    Namespace: Parsed arguments.

                Raises:
                    HTTPException: If there is an error parsing the arguments.
                """
        try:
            parser = reqparse.RequestParser()
            parser.add_argument('text', type=str, required=True, help='Text is required.')
            parser.add_argument('token', type=str, required=True, help='Token is required.')
            return parser.parse_args()
        except Exception as e:
            self.abort_with_error(f"Error parsing arguments: {str(e)}", 400)
