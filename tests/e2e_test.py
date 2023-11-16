import json
import pytest
from app import create_app, db
from api.models.log_entry import LogEntry


@pytest.fixture
def apps():
    """Create and configure a new app instance for each test."""
    apps = create_app()
    apps.config['TESTING'] = True
    with apps.app_context():
        db.create_all()
    yield apps


@pytest.fixture
def client(apps):
    """A test client for the app."""
    return apps.test_client()


def test_logging_to_database(client):
    # Make a sample request that logs information
    response = client.post('/encrypt', json={'text': 'sample_text', 'token': 'sample_token'})
    assert response.status_code == 200

    # Check if the log entry is present in the database
    logs = LogEntry.query.all()
    assert len(logs) == 1
    assert logs[0].level == 'INFO'
    assert logs[0].message == 'INFO: Logging information'


def test_logging_error_to_database(client):
    # Make a sample request that logs an error
    response = client.post('/decrypt', json={'text': 'sample_text', 'token': 'invalid_token'})
    assert response.status_code == 500

    # Check if the error log entry is present in the database
    logs = LogEntry.query.all()
    assert len(logs) == 1
    assert logs[0].level == 'ERROR'
    assert logs[0].message == 'ERROR: Logging error'
