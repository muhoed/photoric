from flask import Blueprint


# Blueprint initialization
albums_bp = Blueprint('albums', __name__,
                   url_prefix='/albums',
                   template_folder='templates',
                   static_folder='static',
                   static_url_path='/static')


from photoric.modules.albums import albums
