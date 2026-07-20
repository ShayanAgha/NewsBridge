import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', '123kjhjkh32891sdlk')
    # Use /tmp/ directory for SQLite if running on Vercel (serverless filesystem is read-only)
    if os.environ.get('VERCEL') == '1' or os.environ.get('VERCEL'):
        SQLALCHEMY_DATABASE_URI = 'sqlite:////tmp/newsbridge.db'
    else:
        SQLALCHEMY_DATABASE_URI = 'sqlite:///newsbridge.db'

    # Required for SQLite under multi-threaded serverless request handling
    SQLALCHEMY_ENGINE_OPTIONS = {
        'connect_args': {'check_same_thread': False},
    }
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    API_BEARER_TOKEN = os.environ.get('API_BEARER_TOKEN', '1920391u')
    ADMIN_USERNAME = os.environ.get('ADMIN_USERNAME', 'admin')
    ADMIN_PASSWORD = os.environ.get('ADMIN_PASSWORD', 'admin123')
