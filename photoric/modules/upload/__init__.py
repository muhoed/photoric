""" Initialize upload module """
from flask import Blueprint
from photoric.flask_uploads.flask_uploads import UploadSet, IMAGES
from flask_dropzone import Dropzone


# Blueprint initialization
upload_bp = Blueprint('upload', __name__,
                   url_prefix='/upload',
                   template_folder='templates',
                   static_folder='static',
                   static_url_path='/static')


# setup upload set and dropzone instances
photos = UploadSet('photos', IMAGES)
dropzone = Dropzone()


from photoric.modules.upload import upload
