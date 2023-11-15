# tests/e2e_test.py

import unittest
from unittest.mock import patch
from flask import Flask
from flask_restful import Api
from app.resources.resources import TokenResource, EncryptionResource, DecryptionResource, LogResource, BaseResource


import sys
print(sys.path)


class TestBaseResource(unittest.TestCase):
    def setUp(self):
        self.app = Flask(__name__)
        self.api = Api(self.app)
        self.api.add_resource(BaseResource, '/base')

    def test_abort_with_error(self):
        with self.app.test_client() as client:
            response = client.get('/base')
            self.assertEqual(response.status_code, 400)
            self.assertEqual(response.json, {'message': 'Text not provided.'})

    def test_process_text_with_valid_input(self):
        with self.app.test_client() as client:
            response = client.post('/base', json={'text': 'sample', 'token': 'fake_token'})
            self.assertEqual(response.status_code, 200)

    def test_process_text_with_empty_text(self):
        with self.app.test_client() as client:
            response = client.post('/base', json={'text': '', 'token': 'fake_token'})
            self.assertEqual(response.status_code, 400)
            self.assertEqual(response.json, {'message': 'Text not provided.'})

    def test_process_text_with_empty_token(self):
        with self.app.test_client() as client:
            response = client.post('/base', json={'text': 'sample', 'token': ''})
            self.assertEqual(response.status_code, 400)
            self.assertEqual(response.json, {'message': 'Token not provided.'})

    def test_process_text_with_exception(self):
        with patch('cryptography.fernet.Fernet.encrypt', side_effect=Exception('Test exception')):
            with self.app.test_client() as client:
                response = client.post('/base', json={'text': 'sample', 'token': 'fake_token'})
                self.assertEqual(response.status_code, 500)


class TestTokenResource(unittest.TestCase):
    def setUp(self):
        self.app = Flask(__name__)
        self.api = Api(self.app)
        self.api.add_resource(TokenResource, '/token')

    @patch('cryptography.fernet.Fernet.generate_key')
    def test_token_generation(self, mock_generate_key):
        mock_generate_key.return_value = b'fake_token_key'
        with self.app.test_client() as client:
            response = client.get('/token')
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json, {'token': 'fake_token_key'})


class TestEncryptionResource(unittest.TestCase):
    def setUp(self):
        self.app = Flask(__name__)
        self.api = Api(self.app)
        self.api.add_resource(EncryptionResource, '/encrypt')

    @patch('cryptography.fernet.Fernet.encrypt')
    def test_text_encryption(self, mock_encrypt):
        mock_encrypt.return_value = b'encrypted_text'
        with self.app.test_client() as client:
            response = client.post('/encrypt', json={'text': 'sample', 'token': 'fake_token'})
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json, {'encrypted_text': 'encrypted_text'})


class TestDecryptionResource(unittest.TestCase):
    def setUp(self):
        self.app = Flask(__name__)
        self.api = Api(self.app)
        self.api.add_resource(DecryptionResource, '/decrypt')

    @patch('cryptography.fernet.Fernet.decrypt')
    def test_text_decryption(self, mock_decrypt):
        mock_decrypt.return_value = b'decrypted_text'
        with self.app.test_client() as client:
            response = client.post('/decrypt', json={'text': 'sample', 'token': 'fake_token'})
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json, {'decrypted_text': 'decrypted_text'})


class TestLogResource(unittest.TestCase):
    def setUp(self):
        self.app = Flask(__name__)
        self.api = Api(self.app)
        self.api.add_resource(LogResource, '/log')

    def test_view_logs(self):
        with open('../logs/api.log', 'w') as log_file:
            log_file.write('Sample log entry')
        with self.app.test_client() as client:
            response = client.get('/log')
            self.assertEqual(response.status_code, 200)
            self.assertIn('Sample log entry', response.json['logs'])

    def test_clear_logs(self):
        with open('../logs/api.log', 'w') as log_file:
            log_file.write('Sample log entry')
        with self.app.test_client() as client:
            response = client.delete('/log')
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json, {'message': 'Log cleared successfully'})
        with open('../logs/api.log', 'r') as log_file:
            logs = log_file.read()
            self.assertEqual(logs, '')


if __name__ == '__main__':
    unittest.main()
