"""Routes for user authentication"""
from flask import Blueprint, request, redirect, render_template, flash
from flask_uploads import UploadSet, IMAGES
from flask_dropzone import Dropzone
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms import SubmitField

from photoric.modules.core.images.images import create_image


# Blueprint initialization
upload = Blueprint('upload', __name__,
                   url_prefix='/upload',
                   template_folder='templates',
                   static_folder='static',
                   static_url_path='/static')

# setup upload set and dropzone instances
photos = UploadSet('photos', IMAGES)
dropzone = Dropzone()


""" upload form """


class UploadButton(FlaskForm):
    """Images upload form"""
    photo = FileField(
        validators=[
            FileAllowed(photos, message='Only files of valid image formats (i.e. .jpg, .jpeg, .png, .tiff etc.) \
            are allowed'),
            FileRequired('File is empty')
        ]
    )

    submit = SubmitField('Add')


""" add upload form to templates through context processor """


@upload.app_context_processor
def upload_form():
    """ inflect upload form to templates """
    return dict(upload_form=UploadButton())


""" upload logic routes """


@upload.route('/upload', methods=['GET', 'POST'])
def uploads():
    form = UploadButton()

    # serve request from upload form
    if form.validate_on_submit() or request.method == "POST":
        if 'files[]' not in request.files:
            flash(u'No images were uploaded', "warning")
            return redirect(request.url)
        files = request.files.getlist('files[]')
        files_number = 0
        for file in files:
            filename = photos.save(file)
            url = photos.url(filename)
            create_image(filename, url)
            files_number = +1
        flash(u"%i images were successfully added to the site! You can rename it and add / \
        edit description and keywords at individual image pages or through site administration.".format(files_number),
              "success")
    return render_template("views/index.html")
