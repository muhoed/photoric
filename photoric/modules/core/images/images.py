import iptcinfo3
import os
import datetime

from flask import Blueprint, send_from_directory, abort
from flask_login import current_user
from PIL import Image as Picture
from PIL.ExifTags import TAGS

from photoric.config.config import Config
from photoric.config.models import db, Image
from photoric.modules.core.auth.auth import authorize


# Blueprint initialization
images = Blueprint('images', __name__,
                   url_prefix='/images',
                   template_folder='templates',
                   static_folder='static',
                   static_url_path='/static')


# reverse exif tags dictionary
_TAGS_r = dict(((v, k) for k, v in TAGS.items()))

# path to uploaded images on server
upload_path = os.path.abspath(os.path.join(Config.UPLOADS_DEFAULT_DEST, 'photos'))


@authorize.create(Image)
def create_image(filename, url):

    # read current image with PIL
    with Picture.open(os.path.join(upload_path, filename)) as picture:
        # extract EXIF data
        exifdata = picture.getexif()

    # get exif data to fill image data in db
    try:
        # get shooting date EXIF data
        captured_date = exifdata.get(_TAGS_r['DateTimeOriginal'])

    except:
        captured_date = None

    if captured_date is not None:
        # decode bytes
        if isinstance(captured_date, bytes):
            captured_date = captured_date.decode()
        captured_date = datetime.datetime.strptime(captured_date, '%Y:%m:%d %H:%M:%S')

    try:
        # extract GEOExif data as dictionary, use GEOTAGS to get specific data
        img_location = exifdata.get(_TAGS_r["GSPInfo"])

    except:
        img_location = None

    # get IPTC data
    img_iptc = iptcinfo3.IPTCInfo(os.path.join(upload_path, filename))

    if not img_iptc:
        img_title = None
        img_description = None
        img_keywords = None
    else:
        # get name, description and keywords from IPTC data
        img_title = img_iptc['object name'] or img_iptc['headline']
        if not img_title:
            img_title = filename
        img_description = img_iptc['caption/abstract']
        if not img_description:
            img_description = None
        img_keywords = img_iptc['keywords']
        if not img_keywords:
            img_keywords = None

    # get current user data
    user_id = current_user.id
    
    for group in current_user.groups:
        if group is not None:
            group_id = group.id
            break

    # create image object
    image = Image(
        name=img_title,
        filename=filename,
        url=url,
        description=img_description,
        keywords=img_keywords,
        captured_on=captured_date,
        location=img_location,
        owner_id=user_id,
        group_id=group_id
    )

    try:
        # save image to database
        db.session.add(image)
        db.session.commit()

    except:
        abort(400)

    return True


# return image from url
@images.route('/photos/<filename>')
def get_image(filename):
    return send_from_directory(upload_path, filename)
