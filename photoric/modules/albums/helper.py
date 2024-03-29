from photoric.core.models import Album


# get album by name
def get_album_by_name(name):
    return Album.query.filter_by(name=name).first()

# get album by id
def get_album_by_id(id):
    return Album.query.filter_by(id=id).first()
