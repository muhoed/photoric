"""Routes for user authentication"""
from flask import request, redirect, render_template, flash, session, url_for

from photoric.modules.auth import authorize
from photoric.modules.images import create_image
from photoric.core.models import Album
from photoric.modules.upload.forms import UploadButton
from photoric.modules.upload import upload_bp


# save image and return parameters required to store its information in database
@authorize.in_group('contributors')
def save_image(file):
    filename = photos.save(file)
    url = photos.url(filename)
    if create_image(filename, url):
        return True
    flash(u'Error occurs during adding image(-es) to database', "danger")
    return redirect(request.url)


# add upload form to templates through context processor
@upload_bp.app_context_processor
def upload_form():
    """ inflect upload form to templates """
    return dict(upload_form=UploadButton())


""" upload logic routes """


@upload_bp.route('/uploads', methods=['GET', 'POST'])
@authorize.in_group('contributors')
def uploads():
    form = UploadButton()
    files_number = 0
    # serve request from upload form
    if form.validate_on_submit():
        # if 'files[]' not in request.files:
        #    flash(u'No images were uploaded', "warning")
        #    return redirect(request.url)
        # files = request.files.getlist('files[]')
        for file in form.photo.data:
            if save_image(file):
                files_number += 1  # files_number + 1
    # serve request from dropzone
    # elif request.method == "POST":
        for key, file in request.files.items():
            if key.startswith('file'):
                if save_image(file):
                    files_number += 1  # files_number + 1
    # redirect to home page in case of GET method
    else:
        return render_template("views/index.html", title='Home page')

    flash(u"{} images were successfully uploaded! You can rename it and add / \
    edit description and keywords at individual image pages or through site administration.".format(files_number),
          "success")
    album_id = session.get("current_album")
    album = Album.query.filter_by(id=int(album_id)).first()
    # save album name to session for dropzone redirect function
    session["album_name"] = album.name
    if album:
        return redirect(url_for("albums.show_album", album_name=album.name))
    return redirect(url_for("views.index"))


# redirect to home page in case of dropzone errors
@upload_bp.route("/index")
def index():
    return redirect(url_for('views.index'))
