from photoric.config.models import Album


# get album by name
def get_album_by_name(name):
    return Album.query.filter_by(name=name).first()
