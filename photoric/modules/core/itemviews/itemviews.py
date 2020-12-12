from flask import Blueprint, session, render_template, request, url_for, flash

from ..helpers.database.db import get_gallery_items

item_views = Blueprint('itemviews', __name__, url_prefix='/')

@itemviews.route("/", methods=['GET', 'POST'])
@itemviews.route("/index", methods=['GET', 'POST'])
def index():
    """Show main page"""

    user_id = session.get("user_id")

    # page was loaded after some actions performed
    if request.method == "POST":
        return TODO

    # page was loaded without action
    else:

        # get view items and load page
        return render_template('index.html', gallery_items = gallery_items)

    
            
    
