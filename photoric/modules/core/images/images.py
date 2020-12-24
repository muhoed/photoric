from flask import Blueprint
from PIL import Image
from PIL.ExifTags import TAGS

from photoric.config.models import Image


# Blueprint initialization
images = Blueprint('images', __name__,
                   url_prefix='/images',
                   template_folder='templates',
                   static_folder='static',
                   static_url_path='/static')


def create_image(filename, url):
    # read current image with PIL
    imagename = url
    image = Image.open(imagename)

    # extract EXIF data
    exifdata = image.getexif()
    # read EXIF data
    for tag_id in exifdata:
        tag = TAGS.get(tag_id, tag_id)
        data = exifdata.get(tag_id)
        #decode bytes
        if isinstance(data, bytes):
            data = data.decode()
    captured_on = exifdata('DataTimeOriginal')

