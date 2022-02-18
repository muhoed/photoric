""" Initialize Search module """
from flask import Blueprint


# Blueprint initialization
search_bp = Blueprint(
    'search', __name__,
    url_prefix='/search',
    template_folder='templates',
    static_folder='static',
    static_url_path='/static'
)


from photoric.modules.search import search
