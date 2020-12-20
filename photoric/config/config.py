"""Flask config."""
from os import environ, path
from dotenv import load_dotenv
from tempfile import mkdtemp

basedir = path.abspath(path.dirname(__file__))
load_dotenv(path.join(basedir, '.env'))


class Config:
    """Base config."""
    
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

    # Recaptcha config for forms
    RECAPTCHA_PUBLIC_KEY = 'to be added'
    RECAPTCHA_PRIVATE_KEY = 'to be added'

    # Views specific variables
    SITE_NAME = 'Photoric'


class ProdConfig(Config):
    """Production specific config."""
    SECRET_KEY = 'production'  # environ.get('SECRET_KEY')

    if not SECRET_KEY:
        raise ValueError("No SECRET_KEY set for Flask application")

    FLASK_ENV = 'production'
    FLASK_DEBUG = False
    FLASK_TESTING = False
    SQLALCHEMY_DATABASE_URI = environ.get('PROD_DATABASE_URI')


class DevConfig(Config):
    """Development specific config."""
    SECRET_KEY = 'development'
    FLASK_ENV = 'development'
    FLASK_DEBUG = True
    FLASK_TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"  # 'sqlite:///' + path.join(basedir,  'photoric.db')
