import os
import pytest
import tempfile

from photoric import create_app, db


@pytest.fixture
def client():
    app = create_app("test")

    #app.config["TESTING"] = True
    #app.testing = True

    # This creates an in-memory sqlite db
    #app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite://"

    #db_fd, db_path = tempfile.mkstemp()

    #app.config.update({"SQLALCHEMY_DATABASE_URI" : db_path})

    #client = app.test_client()
    with app.app_context():
        #create test database
        db.create_all()
        
        # filters and variables for jinja2 templates
        @app.template_global()
        def site_name():
            return app.config['SITE_NAME']

        # initial setup
        from photoric.config.initial_setup import initial_setup
        app.before_first_request(initial_setup)

    yield app

    #os.close(db_fd)
    #os.unlink(db_path)

@pytest.fixture
def client(app):
    return app.test_client()