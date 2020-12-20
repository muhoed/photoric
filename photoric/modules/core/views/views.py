from flask import Blueprint, render_template, request

from .helper import get_gallery_items


views = Blueprint('views', __name__, url_prefix='/views')


@views.route("/", methods=['GET', 'POST'])
@views.route("/index", methods=['GET', 'POST'])
def index():
    """Show main page"""

    # page was loaded after some actions performed
    if request.method == "POST":
        return TODO

    # page was loaded without action
    else:
        # get top-level gallery items from database
        gallery_items = get_gallery_items('no', '')

        # if user is not admin show gallery items if any
        return render_template('views/index.html', title='home page', gallery_items=gallery_items)

        # if user is admin gallery_items is not None load admin version of the page

        # if user is admin and get view items is None load dropzone page to upload
