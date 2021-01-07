"""Routes for search functions"""
import re
from flask import Blueprint, render_template, redirect, url_for

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
    if form.validate_on_submit():
        text = form.text.data
        albums_search = []
        images_search = []
        words = re.findall(r"[^,;\s]+", text)
        for word in words:
            albums, images = search_gallery_items(word)
            albums_search.extend(albums)
            images_search.extend(images)
        return render_template(url_for('views/index.html', title='search results', albums=albums_search, images=images_search))
    return redirect(request.url)
