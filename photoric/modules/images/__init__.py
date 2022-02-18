""" Initialize image handilng module """
from flask import Blueprint


# Blueprint initialization
images_bp = Blueprint('images', __name__,
                   url_prefix='/images',
                   template_folder='templates',
                   static_folder='static',
                   static_url_path='/static')


from photoric.modules.images import images
