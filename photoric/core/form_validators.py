from wtforms.validators import ValidationError

# from photoric.modules.core.albums.helper import get_album_by_name
# from photoric.modules.core.images.helper import get_image_by_name
from photoric.core.models import check_object_name

""" custom form validators to use with wtforms """


# validator to check whether name exists
class NameExists(object):
    def __init__(self, item_type=None, message=None):
        if not item_type:
            item_type = 'album'
        self.item_type = item_type
        if not message:
            message = u'The %s with such name already exists' % item_type
        self.message = message

    def __call__(self, form, field):
        name = field.data or None
        if check_object_name(self.item_type, name):
            raise ValidationError(self.message)


# initialize name check validator
name_check = NameExists