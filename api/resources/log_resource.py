# /your_project/api/resources/log_resource.py
from .base_resource import BaseResource
from app.app import db
from api.models.log_entry import LogEntry
from .. import api_blueprint


@api_blueprint.route('/log')
class LogResource(BaseResource):
    def get(self):
        logs = LogEntry.query.all()
        return {'logs': [{'message': log.message, 'level': log.level} for log in logs]}, 200

    def delete(self):
        LogEntry.query.delete()
        db.session.commit()
        return {'message': 'Log cleared successfully'}, 200
