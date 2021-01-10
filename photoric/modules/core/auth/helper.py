from flask_sqlalchemy import SQLAlchemy

from photoric.config.models import db, Image, Album, User


# get user by name or list all registered users
def get_user_by_name(name = 'all'):
    if name != 'all':
        requested_user = User.query.filter_by(name=name).first()
    else:
        requested_user = User.query.all()

    return requested_user
