import os

from flask import Flask
from flask_session import Session
from flask_sqlalchemy import SQLAlchemy


from .config import config
from .modules.core.helpers.form.forms import SimpleSearch

def create_app(conf='dev'):
    # Initialize core application and load configuration
    app = Flask(__name__, instance_relative_config=True)
    
    if conf is 'dev':
        app.config.from_object(config.DevConfig)
    else:
        app.config.from_object(config.ProdConfig)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # Ensure responses aren't cached
    #@app.after_request
    #def add_header(response):
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
    from .config.models import login_manager
    login_manager.init_app(app)
    
    with app.app_context():
        # register blueprints with views
        # from .modules.core.modfactory import modfactory
        from .modules.core.views import views
        from .modules.core.auth import auth
        from .modules.core.nav import nav
        from .modules.core.search import search

        # app.register_blueprint(modfactory.modfactory)
        app.register_blueprint(itemviews.itemviews)
        app.register_blueprint(auth.auth)
        app.register_blueprint(nav.nav)
        app.register_blueprint(search.search)

        # extensions settings
        login_manager.login_view = "auth.signin"

        # initialize processors
        # global functions for jinja templates
        #from .modules.core.helpers.processors.context_processors import processors
        #app.context_processor(processors)

        # create database
        db.create_all()

        return app
