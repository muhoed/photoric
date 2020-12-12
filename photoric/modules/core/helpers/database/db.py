from flask_sqlalchemy import SQLAlchemy

from photoric.config.models import db, GalleryItem, Image, Album


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
        return requested.filter_by(parent.id == int(parent)).all()
    elif parent =='all':
        """ return all items of requested type """
        return requested.all()
    else:
        """ return all top-level (without parent item) items of requested type """
        return requested.filter_by(parent is NULL).all()
        
