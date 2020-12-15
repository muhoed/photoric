from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import with_polymorphic

from photoric.config.models import db, GalleryItem, Image, Album, User


# get gallery items
def get_gallery_items(parent = 'all', item = 'all'):

    """ request gallery items of spepcific type """ 
    if item == 'album':
        requested = db.session.query(Album)
    elif item == 'image':
        requested = db.session.query(Image)
    else:
        requested = db.session.query(GalleryItem) 

    if isinstance(int(parent), int):
        """ return all items of requested type for specific parent item """
        return requested.filter_by(parent_id = int(parent)).all()
    elif parent =='all':
        """ return all items of requested type """
        return requested.all()
    else:
        """ return all top-level (without parent item) items of requested type """
        return requested.filter_by(parent_id is NULL).all()

        
# get menu
def get_menu(menu):
    # query respective database table
    return Menu.query.filter_by(type = menu).all()


# get user by name or list all reqistered users
def get_user_by_name(name = 'all'):
    if name != 'all':
        requested_user = User.query.filter_by(name=name).first()
    else:
        requested_user = User.query.all()

    return requested_user
