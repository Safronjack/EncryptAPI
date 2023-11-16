import json
import pytest
from cryptography.fernet import Fernet
from flask import Flask
from flask_restful import Api

token = ''
text = ''
word = 'Secret dungeon.'

flask_app = Flask(__name__)
api = Api(flask_app)


def create_app():
    return flask_app, api


@pytest.fixture
def app():
    """Fixture to create the Flask app."""
    return flask_app


@pytest.fixture
def client(app):
    """Fixture to create a test client for the Flask app."""
    return app.test_client()


def test_e2e(client):
    """End-to-End test for token generation, encryption, and decryption."""
    global token
    # Sending a POST request to /token
    response = client.get('https://localhost/token')  # Обратите внимание на использование https

    # Checking the response code and format
    assert response.status_code == 200
    result = json.loads(response.data.decode('utf-8'))
    token = result['token']
    assert 'token' in result

    # Creating a test request
    key = Fernet.generate_key()
    data = {'text': word, 'token': token}

    # Sending a POST request to /encrypt
    response = client.post('https://localhost/encrypt', json=data)  # Используйте https

    # Checking the response code and format
    assert response.status_code == 200
    result = json.loads(response.data.decode('utf-8'))
    text = result['encrypted_text']
    assert 'encrypted_text' in result

    # Sending a POST request to /decrypt
    response = client.post('https://localhost/decrypt', json={'text': text, 'token': token})  # Используйте https

    # Checking the response code and format
    assert response.status_code == 200
    result = json.loads(response.data.decode('utf-8'))
    assert 'decrypted_text' in result
    assert result['decrypted_text'] == word

def test_successful_encryption(client):
    """Test for successful encryption."""
    # Generating a key and creating a test request
    key = Fernet.generate_key()
    data = {'text': 'Hello, World!', 'token': key.decode()}

    # Sending a POST request to /encrypt
    response = client.post('https://localhost/encrypt', json=data)

    # Checking the response code and format
    assert response.status_code == 200
    result = json.loads(response.data.decode('utf-8'))
    assert 'encrypted_text' in result

def test_encryption_missing_text(client):
    """Test for encryption with missing text."""
    # Sending a POST request to /encrypt without specifying text
    response = client.post('https://localhost/encrypt', json={'token': 'some_token'})

    # Checking the response code and format
    assert response.status_code == 400
    result = json.loads(response.data.decode('utf-8'))
    assert 'error' in result

def test_encryption_missing_token(client):
    """Test for encryption with missing token."""
    # Sending a POST request to /encrypt without specifying a token
    response = client.post('https://localhost/encrypt', json={'text': 'some_text'})

    # Checking the response code and format
    assert response.status_code == 400
    result = json.loads(response.data.decode('utf-8'))
    assert 'error' in result

def test_encryption_valid_input(client):
    """Test for encryption with valid input."""
    # Sending a POST request to /encrypt with correct parameters
    response = client.post('https://localhost/encrypt',
                           json={'text': 'some_text', 'token': 'JREvBAi0px-s18i9odS5aMhK-86w4u_ON7vmLoWRT54='})

    # Checking the response code and format
    assert response.status_code == 200
    result = json.loads(response.data.decode('utf-8'))
    assert 'encrypted_text' in result


def test_encryption_empty_request(client):
    """Test for encryption with an empty request."""
    # Sending a POST request to /encrypt without a request body
    response = client.post('https://localhost/encrypt')

    # Checking the response code and format
    assert response.status_code == 415
    result = json.loads(response.data.decode('utf-8'))
    assert 'error' in result


def test_decryption_missing_encrypted_text(client):
    """Test for decryption with missing encrypted text."""
    # Sending a POST request to /decrypt without specifying encrypted text
    response = client.post('https://localhost/decrypt', json={'token': 'some_token'})

    # Checking the response code and format
    assert response.status_code == 400
    result = json.loads(response.data.decode('utf-8'))
    assert 'error' in result


def test_decryption_missing_token(client):
    """Test for decryption with missing token."""
    # Sending a POST request to /decrypt without specifying a token
    response = client.post('https://localhost/decrypt', json={
        'encrypted_text': 'gAAAAABlVfIWrrm3duij_hq9tMEjS0VD-1vzeN_ZxCDnhi3ZrvEIqai-bU53erCH8aEJaEF7-ygMQovOiHTP67CozAgytTMAPw=='})

    # Checking the response code and format
    assert response.status_code == 400
    result = json.loads(response.data.decode('utf-8'))
    assert 'error' in result
