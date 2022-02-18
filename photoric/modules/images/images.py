import iptcinfo3
import os
import datetime

from flask import send_from_directory, abort, session, redirect, url_for, render_template
from flask_login import current_user
from PIL import Image as Picture
from PIL.ExifTags import TAGS

from photoric.config.config import Config
from photoric import db
from photoric.core.models import Image
from photoric.modules.auth import authorize
from photoric.modules.albums.helper import get_album_by_id
from photoric.modules.images.helper import get_image_by_name, decode_bytes
from photoric.modules.views.helper import get_gallery_items
from photoric.modules.images import images_bp


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

        img_title = decode_bytes(img_title)
            
        img_description = img_iptc['caption/abstract']
        if not img_description:
            img_description = None

        img_description = decode_bytes(img_description)
            
        keywords_list = img_iptc['keywords']
        img_keywords = ''
        if not keywords_list:
            img_keywords = None
        else:
            for keyword in keywords_list:
                keyword = decode_bytes(keyword)
                img_keywords = img_keywords + ', ' + keyword    


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

    # get parent album
    parent_id = session.get("current_album")
    if parent_id is not None:
        image.parent_id = int(parent_id)

    try:
        # save image to database
        db.session.add(image)
        db.session.commit()

    except:
        abort(400)

    return True


# return image from url
@images_bp.route('/photos/<filename>')
def get_image(filename):

    # return image file if image exists and user is authorised to read it
    image = Image.query.filter_by(filename=filename).first()
    if image:
        if authorize.read(image):
            return send_from_directory(upload_path, filename)
        else:
            raise Unauthorized
    raise NotFound


# route to show individual image view
@images_bp.route('/<image_name>')
@authorize.read
def show_image(image_name):

    # get image object to display
    image = get_image_by_name(image_name)

    if image:

        # get parent album and siblings if any
        if image.parent_id is not None:
            parent_album = get_album_by_id(image.parent_id)
            siblings = parent_album.children_images
        else:
            parent_album = None
            siblings = get_gallery_items(parent_album, 'images')
    
        return render_template('images/image_view.html',
                               current_image=image,
                               parent_album=parent_album,
                               siblings=siblings,
                               title='Image: ' + image.name)

    # redirect to home page if image is not found
    return redirect(url_for('views.index'))
