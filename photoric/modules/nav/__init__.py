""" Initialize navbar generator module """
from flask import Blueprint


# Blueprint initialization
nav_bp = Blueprint(
    'nav', __name__,
    template_folder='templates',
    static_folder='static',
    static_url_path='/static',
    url_prefix='/nav'
)


from photoric.modules.nav import nav
