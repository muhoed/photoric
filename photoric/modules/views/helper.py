from sqlalchemy import or_

from photoric.core.models import db, Image, Album


# get gallery items
def get_gallery_items(parent=None, item='albums'):

    """ request gallery items of specific type """
    if item == 'albums':
        if parent is None:
            return Album.query.filter(Album.parent_id == None, Album.authorized('read')).all()
        elif isinstance(parent, int):
            return Album.query.filter(Album.parent_id == parent, Album.authorized('read')).all()
        else:
            return Album.query.filter(Album.authorized('read')).all()
    else:
        if parent is None:
            return Image.query.filter(Image.parent_albums == None, Image.authorized('read')).all()
        elif isinstance(parent, int):
            return db.session.query(Image).\
                   options(selectinload('parent_albums')).\
                   filter(Album.album_id==parent, Image.authorized('read')).all()  # Image.query.filter(Image.parent_id == parent, Image.authorized('read')).all()
        else:
            return Image.query.filter(Image.authorized('read')).all()



    """ polymorthic should be corrected
    if item == 'album':
        requested = db.session.query(Album)
    elif item == 'image':
        requested = db.session.query(Image)
    else:
        requested = db.session.query(GalleryItem)

    if requested is None:
        return None
    else:
        if isinstance(parent, int):
            # return all items of requested type for specific parent item
            return requested.with_polymorphic([Image, Album]).filter(or_(Image.parent_id is None,
                                                                         Album.parent_id is None)).all()
        elif parent == 'all':
            # return all items of requested type
            return requested.all()
        else:
            # return all top-level (without parent item) items of requested type
            return requested.filter(Image.parent_id is None).all()
    """
