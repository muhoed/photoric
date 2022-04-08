"""Routes for search functions"""
import re
from flask import render_template, redirect, url_for, request

from photoric.modules.search.forms import SimpleSearch
from photoric.modules.search.helper import search_gallery_items
from photoric.modules.search import search_bp


# initialize custom templates context processors
@search_bp.app_context_processor
def simple_search_form():
    """ inflect search form to templates """
    return dict(search_form=SimpleSearch())


# search routes
@search_bp.route('/simple_search', methods=('GET', 'POST'))
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
        return render_template('views/index.html', title='search results', albums=albums_search, images=images_search)
    return redirect(request.url)
