# /your_project/app/app.py
from app import create_app

flask_app, api = create_app()

if __name__ == '__main__':
    flask_app.run(debug=True)
