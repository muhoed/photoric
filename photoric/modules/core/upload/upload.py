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


# upload form
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


# save image and return parameters required to store its information in database
def save_image(file):
    filename = photos.save(file)
    url = photos.url(filename)
    if create_image(filename, url):
        return True
    flash(u'Error occurs during adding image(-es) to database', "danger")
    return redirect(request.url)


# add upload form to templates through context processor
@upload.app_context_processor
def upload_form():
    """ inflect upload form to templates """
    return dict(upload_form=UploadButton())


""" upload logic routes """


@upload.route('/uploads', methods=['GET', 'POST'])
def uploads():
    form = UploadButton()
    files_number = 0
    # serve request from upload form
    if form.validate_on_submit():
        if 'files[]' not in request.files:
            flash(u'No images were uploaded', "warning")
            return redirect(request.url)
        files = request.files.getlist('files[]')
        for file in files:
            if save_image(file):
                files_number += 1  # files_number + 1
    # serve request from dropzone
    elif request.method == "POST":
        for key, file in request.files.items():
            if key.startswith('file'):
                if save_image(file):
                    files_number += 1  # files_number + 1
    # redirect to home page in case of GET method
    else:
        return render_template("views/index.html", title='Home page')    
    
    flash(u"{} images were successfully added to the site! You can rename it and add / \
    edit description and keywords at individual image pages or through site administration.".format(files_number),
          "success")
    return redirect("views.index")
