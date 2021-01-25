import os

from flask import Flask
from flask_jsglue import JSGlue
from flask_session import Session
from flask_uploads import configure_uploads, patch_request_class
from flask_wtf.csrf import CSRFProtect
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from photoric.config import config


basedir = os.path.abspath(os.path.dirname(__file__))

# create JS integration plugin object
jsglue = JSGlue()

# create db instance
db = SQLAlchemy()

# create migrate instance
migrate = Migrate()

def create_app(conf='dev'):
    # Initialize core application and load configuration
    app = Flask(__name__, instance_relative_config=True)

    if conf == 'dev':
        app.config.from_object(config.DevConfig)
    else:
        app.config.from_object(config.ProdConfig)

    # ensure the instance and storage folders exist
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    try:
        os.makedirs(os.path.join(app.instance_path, 'storage'))
    except OSError:
        pass

    # Ensure responses aren't cached
    @app.after_request
    def add_header(response):
        response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
        response.headers["Expires"] = 0
        response.headers["Pragma"] = "no-cache"
        return response

    # Initialize session
    Session(app)

    # Initialize JS integration plugin
    jsglue.init_app(app)

    # Initialize database
    db.init_app(app)

    # Initialize migration object
    migrate.init_app(app, db)

    # Initialize Login manager
    from photoric.modules.auth import login_manager
    login_manager.init_app(app)

    # Initialize permission control
    from photoric.modules.auth import authorize
    authorize.init_app(app)

    # Initialize admin module
    from photoric.modules.admin import admin_manager
    admin_manager.init_app(app)

    # Initialize API tools
    from photoric.modules.api import mm
    mm.init_app(app)

    # Initialize upload managers
    from photoric.modules.upload import photos, dropzone
    configure_uploads(app, photos)
    app.config['UPLOADED_PHOTOS_DEST'] = os.path.join(app.instance_path, 'storage')
    patch_request_class(app)
    dropzone.init_app(app)
    csrf = CSRFProtect(app)
    
    
    with app.app_context():
        # register blueprints with views
        # from .modules.core.modfactory import modfactory
        from .modules.views import views_bp
        from .modules.auth import auth_bp
        from .modules.nav import nav_bp
        from .modules.search import search_bp
        from .modules.upload import upload_bp
        from .modules.images import images_bp
        from .modules.albums import albums_bp
        from .modules.admin import admin_bp
        from .modules.api import api_bp

        # exclude api routes from WTF csrf protection to avoid error on POST, PUT ...
        csrf.exempt(api_bp)

        # app.register_blueprint(modfactory.modfactory)
        app.register_blueprint(views_bp)
        app.register_blueprint(auth_bp)
        app.register_blueprint(nav_bp)
        app.register_blueprint(search_bp)
        app.register_blueprint(upload_bp)
        app.register_blueprint(images_bp)
        app.register_blueprint(albums_bp)
        app.register_blueprint(admin_bp)
        app.register_blueprint(api_bp)

        # import all models
        # from photoric.core.models import *

        # create database
        # db.create_all()
        
        # filters and variables for jinja2 templates
        @app.template_global()
        def site_name():
            return app.config['SITE_NAME']

        # initial setup
        from .config.initial_setup import initial_setup
        app.before_first_request(initial_setup)

        return app
