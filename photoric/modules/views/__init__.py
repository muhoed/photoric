""" Initialize main views module """
from flask import Blueprint


views_bp = Blueprint('views', __name__,
                  template_folder="templates",
                  static_folder="static",
                  url_prefix='/',
                  static_url_path='/views/static')


from photoric.modules.views import views
