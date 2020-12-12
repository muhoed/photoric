import os

from flask import Flask
from flask_session import Session
from flask_sqlalchemy import SQLAlchemy


from .config import config

def create_app(conf='dev'):
    # Initialize core application and load configuration
    app = Flask(__name__, instance_relative_config=False)
    
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
        # from .modules.core.modfactory import modfactory
        from .modules.core.itemviews import itemviews
        from .modules.core.auth import auth
        from .modules.core.menu import menu

        # initialize custom filter
        #app.jinja_env.filters["usd"] = helpers.usd

        # register blueprints
        # app.register_blueprint(modfactory.modfactory)
        app.register_blueprint(itemviews.item_views)
        app.register_blueprint(auth.auth)
        app.register_blueprint(menu.menu)
        
        # create database
        db.create_all()

        return app
