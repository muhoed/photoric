import os

from flask import Flask
from flask_session import Session
from flask_uploads import configure_uploads, patch_request_class
from flask_wtf.csrf import CSRFProtect

from .config import config


basedir = os.path.abspath(os.path.dirname(__file__))

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
    # @app.after_request
    # def add_header(response):
    #    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    #    response.headers["Expires"] = 0
    #    response.headers["Pragma"] = "no-cache"
    #    return response

    # Initialize session
    Session(app)

    # Initialize database
    from .config.models import db
    db.init_app(app)

    # Initialize Login manager
    from .modules.core.auth.auth import login_manager
    login_manager.init_app(app)

    # Initialize permission control
    from .modules.core.auth.auth import authorize
    authorize.init_app(app)

    # Initialize upload managers
    from .modules.core.upload.upload import photos, dropzone
    configure_uploads(app, photos)
    app.config['UPLOADED_PHOTOS_DEST'] = os.path.join(app.instance_path, 'storage')
    patch_request_class(app)
    dropzone.init_app(app)
    csrf = CSRFProtect(app)
    
    
    with app.app_context():
        # register blueprints with views
        # from .modules.core.modfactory import modfactory
        from .modules.core.views import views
        from .modules.core.auth import auth
        from .modules.core.nav import nav
        from .modules.core.search import search
        from .modules.core.upload import upload

        # app.register_blueprint(modfactory.modfactory)
        app.register_blueprint(views.views)
        app.register_blueprint(auth.auth)
        app.register_blueprint(nav.nav)
        app.register_blueprint(search.search)
        app.register_blueprint(upload.upload)

        # create database
        db.create_all()

        # filters and variables for jinja2 templates
        @app.template_global()
        def site_name():
            return app.config['SITE_NAME']

        # initial setup
        from .config.initial_setup import initial_setup
        app.before_first_request(initial_setup)

        return app
