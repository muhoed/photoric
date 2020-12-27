from sqlalchemy import or_

from photoric.config.models import db, Image, Album


# get gallery items
def get_gallery_items(parent='', item='albums'):

    """ request gallery items of specific type """
    if item == 'albums':
        if parent == 'no':
            return Album.query.filter_by(parent_id=None).all()
        elif isinstance(parent, int):
            return Album.query.filter_by(parent_id=parent).first()
        else:
            return Album.query.all()
    else:
        if parent == 'no':
            return Image.query.filter_by(parent_id=None).all()
        elif isinstance(parent, int):
            return Image.query.filter_by(parent_id=parent).first()
        else:
            return Image.query.all()



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
