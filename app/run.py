# /your_project/run.py
from app.app import app, api

if __name__ == '__main__':
    app.run(debug=True)
