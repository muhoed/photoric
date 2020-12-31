from photoric.config.models import Image
from photoric.modules.core.auth.auth import authorize


# get image by name
@authorize.read
def get_image_by_name(name):
    return Image.query.filter_by(name=name).first()
