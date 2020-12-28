from photoric.config.models import Image


# get image by name
def get_image_by_name(name):
    return Image.query.filter_by(name=name).first()
