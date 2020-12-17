"""Routes for search functions"""
from flask import Blueprint

from .forms import SimpleSearch

# Blueprint initialization
search = Blueprint(
    'search', __name__, url_prefix='/search',
    template_folder='templates',
    static_folder='static'
)

""" initialize custom templates context processors """
@search.app_context_processor()
def simple_search_form():
    """ inflect search form to templates """
    return dict(search_form=SimpleSearch())

@search.simple_search('/simple_search', methods=('GET', 'POST'))
def simple_search():
    # TODO
