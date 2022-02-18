from wtforms.validators import ValidationError

# from photoric.modules.core.albums.helper import get_album_by_name
# from photoric.modules.core.images.helper import get_image_by_name
from photoric.core.models import Album

""" custom form validators to use with wtforms """


# validator to check whether name exists
class NameExists(object):
    def __init__(self, cls=None, message=None):
        if not cls:
            cls = Album
        self.cls = cls
        if not message:
            message = u'The %s with such name already exists' % cls.__name__.tolower()
        self.message = message

    def __call__(self, form, field):
        name = field.data or None
        if self.cls.get_by_name(name=name):
            raise ValidationError(self.message)


# initialize name check validator
name_check = NameExists
