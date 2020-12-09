from flask import Blueprint, session, render_template, request, url_for, flash

from ..helpers.database.db import get_gallery_items

item_views = Blueprint('item_views', __name__, url_prefix='/')

@item_views.route("/", methods=['GET', 'POST'])
@item_views.route("/index", methods=['GET', 'POST'])
def index():
    """Show main page"""

    user_id = session.get("user_id")

    # page was loaded after some actions performed
    if request.method == "POST":
        return TODO

    # page was loaded without action
    else:

        # get view items and load page
        gallery_items = get_gallery_items(parent = 'no_parent')
        return render_template('index.html', gallery_items = gallery_items)

    
            
    
