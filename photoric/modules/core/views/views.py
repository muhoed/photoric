from flask import Blueprint, render_template, request, session

from .helper import get_gallery_items


views = Blueprint('views', __name__,
                  template_folder="templates",
                  static_folder="static",
                  url_prefix='/',
                  static_url_path='/views/static')

# set current active menu item
# session["active"] = "home:"

# context processor to get parent gallery items in template
@views.app_context_processor
def views_processors():

    # get top-level albums
    def get_top_albums():
        return get_gallery_items('no', 'albums')

    # get top-level images
    def get_top_images():
        return get_gallery_items('no', 'images')

    return dict(
        get_top_albums=get_top_albums,
        get_top_images=get_top_images
    )


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
        albums = get_gallery_items('no', 'albums')
        images = get_gallery_items('no', 'images')

        # shares = get_shared_items(current_user.id)

        session["current_album"] = None

        # if user is not admin show gallery items if any
        return render_template('views/index.html', title='Home page', albums=albums, images=images)

        # if user is admin gallery_items is not None load admin version of the page

        # if user is admin and get view items is None load dropzone page to upload


@views.route("/about")
def about():
    return render_template('views/about.html', title='About me')
