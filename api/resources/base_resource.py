# /your_project/api/resources/base_resource.py
from flask import abort, jsonify, request, make_response
from flask_restful import Resource, reqparse
from cryptography.fernet import Fernet
from werkzeug.exceptions import HTTPException


class BaseResource(Resource):
    """
    Base resource class providing common functionality for encryption and decryption resources.
    """

    ERROR_TEXT_NOT_PROVIDED = "Text not provided."
    ERROR_TOKEN_NOT_PROVIDED = "Token not provided."

    def process_text(self, text, token, operation):
        """
        Process the text using the provided operation (encrypt or decrypt).

        Args:
            text (str): The text to be processed.
            token (str): The token used for encryption or decryption.
            operation (callable): The encryption or decryption operation.

        Returns:
            str: The processed text.

        Raises:
            ValueError: If an error occurs during the processing.
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
        Abort the request with a JSON response containing the error message.

        Args:
            message (str): The error message.
            status_code (int): The HTTP status code for the response.

        Raises:
            HTTPException: Always raises an exception to stop further request processing.
        """
        response = make_response(jsonify({'error': message}), status_code)
        abort(response)

    def parse_args(self):
        """
        Parse and validate the request arguments.

        Returns:
            argparse.Namespace: The parsed arguments.

        Raises:
            HTTPException: If there is an error parsing the arguments.
        """
        try:
            parser = reqparse.RequestParser()
            parser.add_argument('text', type=str, required=True, help='Text is required.')
            parser.add_argument('token', type=str, required=True, help='Token is required.')
            args = parser.parse_args(req=request)
            return args
        except HTTPException as e:
            self.abort_with_error(f"Error parsing arguments: {str(e.description)}", e.code)
            return None
