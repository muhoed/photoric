import iptcinfo3

from flask import Blueprint
from PIL import Image
from PIL.ExifTags import TAGS

from photoric.config.models import db, Image


# Blueprint initialization
images = Blueprint('images', __name__,
                   url_prefix='/images',
                   template_folder='templates',
                   static_folder='static',
                   static_url_path='/static')


# reverse exif tags dictionary
_TAGS_r = dict(((v, k) for k, v in TAGS.items()))


def create_image(filename, url):
    # read current image with PIL
    with Image.open(url) as picture:
        # extract EXIF data
        exifdata = picture.getexif()
        img_iptc = iptcinfo3.IPTCInfo(picture)

    # get exif data to fill image data in db
    try:
        # get shooting date EXIF data
        captured_date = exifdata.get(_TAGS_r['DataTimeOriginal'])

    except AttributeError:
        captured_date = None

    if captured_date is not None:
        # decode bytes
        if isinstance(captured_date, bytes):
            captured_date = captured_date.decode()

    try:
        # extract GEOExif data as dictionary, use GEOTAGS to get specific data
        img_location = exifdata.get(_TAGS_r["GSPInfo"])

    except AttributeError:
        img_location = None

    try:
        # get IPTC caption data
        img_title = img_iptc['object name'] or img_iptc['headline']
        img_description = img_iptc['caption/abstract']
        img_keywords = img_iptc['keywords']

    except AttributeError:
        img_title = None
        img_description = None
        img_keywords = None

    # create image object
    if img_title is None:
        name = filename
    else:
        name = img_title

    image = Image(
        name=name,
        filename=filename,
        url=url,
        description=img_description,
        keywords=img_keywords,
        captured_on=captured_date,
        location=img_location
    )

    # save image to database
    db.session.add(image)
    db.session.commit()
