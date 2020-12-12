from flask_sqlalchemy import SQLAlchemy

from photoric.config.models import db, GalleryItem, Image, Album


# get gallery items
def get_gallery_items(parent = 'all', item = 'all'):

    """ return all gallery items """
    if parent == 'all' and item == 'all':
        gallery_items = GalleryItem.query.all()
        return gallery_items

    """ return all albums """
    if parent == 'all' and item == 'album':
        gallery_items = Album.query.all()

    """ return all images """
    if parent == 'all' and item == 'image':
        gallery_items = Image.query.all()

    """ return all top-level (without parent item) gallery items """
    if parent == 'no' and item == 'all':
        gallery_items = GalleryItem.query.filter_by(parent is None).all()
        return gallery_items

    """ return all top-level albums """
    if parent == 'no' and item == 'album':
        gallery_items = Album.query.filter_by(parent is None).all()
        return gallery_items

    """ return all top-level images """
    if parent == 'no' and item == 'image':
        gallery_items = Image.query.filter_by(parent is None).all()
        return gallery_items

    """ return all gallery items for specific parent item """
    if (parent is not 'no' and parent is not 'all') and item == 'all':
        gallery_items = GalleryItem.query.filter_by(parent.id == parent).all()
        return gallery_items

    """ return all albums for specific parent item """
    if (parent is not 'no' and parent is not 'all') and item == 'album':
        gallery_items = Album.query.filter_by(parent.id == parent).all()
        return gallery_items

    """ return all images for specific parent item """
    if (parent is not 'no' and parent is not 'all') and item == 'image':
        gallery_items = Image.query.filter_by(parent.id == parent).all()
        return gallery_items
