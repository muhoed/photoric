"""Flask config."""
from os import environ, path, pardir
from dotenv import load_dotenv
from tempfile import mkdtemp
from pathlib import Path


current_dir = Path(__file__).resolve()
for env_dir in current_dir.parents:
    env_file = Path(path.join(env_dir, '.env'))
    if env_file.exists():
        load_dotenv(env_file)
        break


class Config:
    """Base config"""
    
    # Configure session to use filesystem (instead of signed cookies)
    SESSION_FILE_DIR = mkdtemp()
    SESSION_PERMANENT = False
    SESSION_TYPE = "filesystem"

    # Explicitly set paths
    STATIC_FOLDER = 'static'
    TEMPLATES_FOLDER = 'templates'

    # Database
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = False

    # Flask-Login
    USE_SESSION_FOR_NEXT = True
    REMEMBER_COOKIE_DURATION = 10

    # Flask-Admin
    FLASK_ADMIN_FLUID_LAYOUT = True

    # Flask-Authorize
    AUTHORIZE_DISABLE_JINJA = False
    AUTHORIZE_ALLOW_ANONYMOUS_ACTIONS = True

    # Recaptcha config for forms
    RECAPTCHA_PUBLIC_KEY = 'to be added'
    RECAPTCHA_PRIVATE_KEY = 'to be added'

    # Flask-Uploads and Flask-Dropzone
    UPLOADS_DEFAULT_DEST = path.join('instance', environ.get('PHOTO_STORAGE'))
    UPLOADS_DEFAULT_URL = 'http://127.0.0.1:5000/images/'
    MAX_CONTENT_LENGTH = 256 * 1024 * 1024
    DROPZONE_MAX_FILE_SIZE = 256
    DROPZONE_ALLOWED_FILE_TYPE = 'image'
    DROPZONE_UPLOAD_MULTIPLE = True
    DROPZONE_PARALLEL_UPLOADS = 20
    # DROPZONE_REDIRECT_VIEW = 'views.index'
    DROPZONE_ENABLE_CSRF = True

    # Views specific variables
    SITE_NAME = 'Photoric'


class ProdConfig(Config):
    """Production specific config."""
    SECRET_KEY = environ.get('SECRET_KEY')

    if not SECRET_KEY:
        raise ValueError("No SECRET_KEY set for Flask application")

    FLASK_ENV = 'production'
    FLASK_DEBUG = False
    FLASK_TESTING = False
    SQLALCHEMY_DATABASE_URI = path.join('instance', environ.get('PROD_DATABASE'))


class DevConfig(Config):
    """Development specific config."""
    SECRET_KEY = 'development'
    FLASK_ENV = 'development'
    FLASK_DEBUG = True
    FLASK_TESTING = True
    SQLALCHEMY_DATABASE_URI = environ.get('DEV_DATABASE')
