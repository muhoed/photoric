"""Routes for user authentication"""
from flask import Blueprint
from flask_uploads import UploadSet, IMAGES
from flask_dropzone import Dropzone

from .forms import UploadForm


# Blueprint initialization
upload = Blueprint(
    'upload', __name__,
    url_prefix='/upload',
    template_folder='templates',
    static_folder='static',
    static_url_path='/static'
)

# setup upload set and dropzone instances
photos = UploadSet('photos', IMAGES)
dropzone = Dropzone()



""" initialize custom templates context processors """


@upload.app_context_processor
def upload_form():
    """ inflect upload form to templates """
    return dict(upload_form=UploadForm())


""" upload logic routes """


@upload.route('/upload', methods=['GET', 'POST'])
def upload():
    form = UploadForm()
    if form.validate_on_submit():
        print('to be done')
