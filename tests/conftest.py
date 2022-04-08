#import os
import pytest
#import tempfile

from flask_login import login_user

from photoric import create_app, db
from photoric.modules.auth.models import User


@pytest.fixture(scope='session')
def app():
    """
    Create app instance for tests,initiate, create and clean database instance.
    """
    app = create_app("test")
    
    #app.config["TESTING"] = True
    #app.testing = True

    # This creates an in-memory sqlite db
    #app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite://"

    #db_fd, db_path = tempfile.mkstemp()

    #app.config.update({"SQLALCHEMY_DATABASE_URI" : db_path})

    #client = app.test_client()
    with app.app_context():
        # create test database
        db.create_all()
        
        # filters and variables for jinja2 templates
        @app.template_global()
        def site_name():
            return app.config['SITE_NAME']

        # initial setup
        from photoric.config.initial_setup import initial_setup
        app.before_first_request(initial_setup)

        # test user without admin rights for authenticated requests
        test_user = User(name="test_user", password="test")

        db.session.add(test_user)
        db.session.commit()

        yield app
        
        db.drop_all()

@pytest.fixture
def authenticated_request(app):
    """
    Mock request context and login test_user within it for futher use 
    in tests that require authenicated user exists in session.
    """
    with app.test_request_context():
        # Here we're not overloading the login manager, we're just directly logging in a user
        # with whatever parameters we want. The user should only be logged in for the test,
        # so you're not polluting the other tests.
        yield login_user(User.query.filter_by(name="test_user").first())

@pytest.fixture
def client(app):
    return app.test_client()