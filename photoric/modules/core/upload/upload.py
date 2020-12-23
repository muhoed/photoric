"""Routes for user authentication"""
from flask import Blueprint
from flask_uploads import UploadSet, IMAGES
from flask_dropzone import Dropzone
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms import SubmitField


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
            FileAllowed(photos, message='Only files of valid image formats (i.e. .jpg, .jpeg, .png, .tiff etc.) are allowed'),
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
    if form.validate_on_submit():
        print('to be done')
