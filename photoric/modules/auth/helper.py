# from flask_sqlalchemy import SQLAlchemy

from photoric import db
from photoric.core.models import Image, Album, User
from photoric.core.models import check_object_name


# get user by name or list all registered users
def get_user_by_name(name = 'all'):
    if name != 'all':
        requested_user = User.query.filter_by(name=name).first()
    else:
        requested_user = User.query.all()

    return requested_user


# create new user
def create_user(new_user):

    # replace existing roles with respective db instances
    if new_user.roles is not None:
        roles=new_user.roles
        new_user.roles = []
        for role in roles:
            existing_role = check_object_name(object_type='role', name=role.name)
            if existing_role:
                new_user.roles.append(existing_role)
            else:
                new_user.roles.append(role)
            
    # replace existing groups with respective db instances
    if new_user.groups is not None:
        groups=new_user.groups
        new_user.groups = []
        for group in groups:
            existing_group = check_object_name(object_type='group', name=group.name)
            if existing_group:
                new_user.groups.append(existing_group)
            else:
                new_user.groups.append(group)

    # write new user to database
    db.session.add(new_user)
    db.session.commit()

    created_user = get_user_by_name(name=new_user.name)

    # return created user object
    return created_user

# update user details: name/email/password/roles/groups
def update_user(data):
    pass
