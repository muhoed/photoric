from photoric.config.models import db, Album, Image


def search_gallery_items(word):
    if word:
        albums = Album.query.filter(Album.name.like('%' + word + '%'),
                                    Album.description.like('%' + word + '%'),
                                    Album.keywords.like('%' + word + '%')).all()
        images = Image.query.filter(Image.name.like('%' + word + '%'),
                                    Image.description.like('%' + word + '%'),
                                    Image.keywords.like('%' + word + '%')).all()
        return albums, images
