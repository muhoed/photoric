from flask import Blueprint, session, render_template, request, url_for, flash

from ..helpers.database.queres import get_user, get_categories, get_albums, get_images

iv = Blueprint('itemviews', __name__, url_prefix='/')

@iv.route("/", methods=['GET', 'POST'])
@iv.route("/index", methods=['GET', 'POST'])
def index():
    """Show main page"""

    user_id = session.get("user_id")

    # page was loaded after some actions performed
    if request.method == "POST":
        return TODO

    # page was loaded without action
    else:
        user_access = 'public'
        # user is logged in
        if user_id:
            user_access = get_user(user_id, user_access)

        # get view items and load page
        categories = get_categories(user_access)
        albums = get_albums(user_access, "top")
        images = get_images(user_access, "top")
        return render_template('index.html', categories = categories, albums = albums, images = images)

    
            
    
