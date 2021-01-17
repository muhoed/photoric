from flask_sqlalchemy import SQLAlchemy

from photoric.core.models import db, Image, Album, User


# get user by name or list all registered users
def get_user_by_name(name = 'all'):
    if name != 'all':
        requested_user = User.query.filter_by(name=name).first()
    else:
        requested_user = User.query.all()

    return requested_user

# create new user
def create_user(data):

    # prepare user object
    new_user =  User(
        name = data.get("name"),
        email = data.get("email")
    )
    new_user.set_password(data.get("password"))
    if data.get("roles"):
        new_user.roles.append(data.get("roles"))
    if data.get("groups"):
        new_user.roles.append(data.get("groups"))

    # write new user to database
    db.session.add(new_user)
    db.session.commit()

    created_user = get_user_by_name(name=new_user.name)

    # return created user object
    return created_user
