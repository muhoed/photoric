""" Initialize authentication and authorization module """
from flask import Blueprint
from flask_login import LoginManager
from flask_authorize import Authorize


# Blueprint initialization
auth_bp = Blueprint(
    'auth', __name__,
    url_prefix='/auth',
    template_folder='templates',
    static_folder='static',
    static_url_path='/static'
)


# setup LoginManager object
login_manager = LoginManager()
login_manager.login_view = "auth.signin"

# setup Authorize object
authorize = Authorize()


from photoric.modules.auth import auth
