from flask import redirect, url_for, session, flash, render_template
from flask_login import current_user

from photoric.modules.albums.forms import CreateAlbumForm
from photoric.modules.auth.auth import authorize
from photoric import db
from photoric.core.models import Album, Image
from photoric.modules.views.helper import get_gallery_items
from photoric.modules.albums import albums_bp


# create album form context processor
@albums_bp.app_context_processor
def create_album_form():
    return dict(create_album_form=CreateAlbumForm())


# db context processors
@albums_bp.app_context_processor
def albums_processors():
    # get list of all albums
    def list_albums():
        return Album.query.filter(Album.authorized('read')).all()

    # get number of images in album
    def get_elements_number(album_id):
        album_content = {}
        album_content['albums'] = get_gallery_items(album_id, 'albums').count() # Album.query.filter(Album.parent_id == album_id).count()
        album_content['images'] = get_gallery_items(album_id, 'images').count() # Image.query.filter(Image.parent_id == album_id).count()
        return album_content

    return dict(list_albums=list_albums,
                get_elements_number=get_elements_number
                )


# route for album creation
@authorize.create(Album)
@albums_bp.route("/create", methods = ['GET', 'POST'])
def create_album():
    form = CreateAlbumForm()
    parent = session.get("current_album")
    if form.validate_on_submit():
        
        # get current user data
        user_id = current_user.id

        for group in current_user.groups:
            if group is not None:
                group_id = group.id
                break

        # generate new album object
        new_album = Album(
                        name=form.name.data,
                        description=form.description.data,
                        keywords=form.keywords.data,
                        parent_id=parent,
                        owner_id=user_id,
                        group_id=group_id
                    )
        db.session.add(new_album)
        db.session.flush()

        # write new album id in session
        session["current_album"] = new_album.id
        session["album_name"] = new_album.name

        # write new album to database
        db.session.commit()

        # redirect user to album view
        flash (u"Album was successfully created!", "success")
        return redirect(url_for("albums.show_album", album_name=session.get("album_name")))

    # redirect to home page in case of GET method
    flash(u"Create album form was not valid", "danger")
    return render_template("views/index.html", title='Home page')


# route for show album
@albums_bp.route("/<album_name>")
@authorize.read
def show_album(album_name=None):
    if album_name:
        album = Album.query.filter(Album.name == album_name, Album.authorized('read')).first()
        children_albums = get_gallery_items(album.id, 'albums')
        children_images = get_gallery_items(album.id, 'images')
        if not children_albums:
            children_albums = None
        if not children_images:
            children_images = None
        # write id of displayed album
        session["current_album"] = album.id
        session["album_name"] = album.name
        return render_template("views/index.html",
                               title='Album: ' + album_name,
                               albums=children_albums,
                               images=children_images
                               )
    return render_template("views/index.html", title="Home page")


# redirect to show album to serve dropzone redirect
@albums_bp.route("/redirect_to_album")
@authorize.read
def redirect_to_album():
    album_name = session.get("album_name")
    if album_name:
        return redirect(url_for('albums.show_album', album_name=album_name))
    return render_template("views/index.html", title="Home page")
