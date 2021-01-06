"""Routes for search functions"""
import re
from flask import Blueprint

from .forms import SimpleSearch

from photoric.modules.core.search.helper import search_gallery_items


# Blueprint initialization
search = Blueprint(
    'search', __name__,
    url_prefix='/search',
    template_folder='templates',
    static_folder='static',
    static_url_path='/static'
)


""" initialize custom templates context processors """


@search.app_context_processor
def simple_search_form():
    """ inflect search form to templates """
    return dict(search_form=SimpleSearch())

""" view routes """


@search.route('/simple_search', methods=('GET', 'POST'))
def simple_search():
    form = SimpleSearch()
    if form.validate_on_submin():
        text = form.text.data
        albums = []
        images= []
        words = re.findall(r"[^,;\s]+", text)
        for word in words:
            search_gallery_items(word)
            albums.extend(albums)
            images.extend(images)
        for album in albums:
            albums


