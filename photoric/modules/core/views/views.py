from flask import Blueprint, render_template, request, session, abort

from .helper import get_gallery_items
from photoric.config.models import Album, Image


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
    def get_children_albums(album_id):
        return get_gallery_items(album_id, 'albums')

    # get top-level images
    def get_children_images(album_id):
        return get_gallery_items(album_id, 'images')

    # get gallery item by id
    def get_gallery_item_by_id(item_id=None, item_type='album'):
        if item_id:
            if item_type == 'album':
                return Album.query.filter_by(id=item_id).first()
            else:
                return Image.query.filter_by(id=item_id).first()
        return abort(404)

    # get url of the first image in the album
    def get_album_first_image(album_id):
        first_image = Image.query.filter(Image.parent_id == album_id).first()
        if first_image is None:
            first_album = Album.query.filter(Album.parent_id == album_id).first()
            if first_album is not None:
                first_image = get_album_first_image(first_album.id)
            else:
                first_image = None
        return first_image


    return dict(
        get_gallery_item_by_id=get_gallery_item_by_id,
        get_children_albums=get_children_albums,
        get_children_images=get_children_images,
        get_album_first_image=get_album_first_image
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
        albums = get_gallery_items(None, 'albums')
        images = get_gallery_items(None, 'images')

        # shares = get_shared_items(current_user.id)

        session["current_album"] = None

        return render_template('views/index.html', title='Home page', albums=albums, images=images)


@views.route("/about")
def about():
    return render_template('views/about.html', title='About me')
