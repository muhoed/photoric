from flask import Blueprint, redirect, url_for, session, flash, render_template
from flask_login import current_user

from .forms import CreateAlbumForm
from photoric.modules.core.auth.auth import authorize
from photoric.config.models import db, Album


# Blueprint initialization
albums = Blueprint('albums', __name__,
                   url_prefix='/albums',
                   template_folder='templates',
                   static_folder='static',
                   static_url_path='/static')


# context processor to make create album form available in modals
@albums.app_context_processor
def create_album_form():
    return dict(create_album_form=CreateAlbumForm())

# route for album creation
@authorize.create(Album)
@albums.route("/create", methods = ['GET', 'POST'])
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

        # write new album to database
        db.session.commit()

        # redirect user to album view
        flash (u"Album was successfully created!", "success")
        return redirect(url_for("albums.show_album", album_id=session.get("current_album")))

    # redirect to home page in case of GET method
    flash(u"Create album form was not valid", "danger")
    return render_template("views/index.html", title='Home page')

# route for show album
@authorize.read
@albums.route("/show_album/<int:album_id>")
def show_album(album_id):
    print("to be done")
