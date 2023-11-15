# /your_project/api/models/log_entry.py
from app.app import db


class LogEntry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    message = db.Column(db.String(500), nullable=False)
    level = db.Column(db.String(10), nullable=False)
