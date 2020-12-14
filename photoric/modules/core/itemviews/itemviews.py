from flask import Blueprint, session, render_template, request, url_for, flash
from flask_login import current_user

from photoric.config.models import User
from photoric.modules.core.helpers.database.db import get_gallery_items

itemviews = Blueprint('itemviews', __name__, url_prefix='/')

@itemviews.before_first_request():
def initial_setup():
    # create admin user if not exist
    if get_user('admin') is None:
        

@itemviews.route("/", methods=['GET', 'POST'])
@itemviews.route("/index", methods=['GET', 'POST'])
def index():
    """Show main page"""

    # page was loaded after some actions performed
    if request.method == "POST":
        return TODO

    # page was loaded without action
    else:

        # get view items and load page
        return render_template('index.html', gallery_items = gallery_items)

    
            
    
