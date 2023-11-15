# /your_project/config.py
class Config:
    LOG_FILE = 'logs/api.log'
    LOG_LEVEL = 'DEBUG'

    @staticmethod
    def init_app(app):
        pass
