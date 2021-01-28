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

# fill in user roles and groups
def fill_roles_groups(user):
    # replace existing roles with respective db instances
    if user.roles:
        roles=user.roles
        user.roles = []
        for role in roles:
            existing_role = check_object_name(object_type='role', name=role.name)
            if existing_role:
                user.roles.append(existing_role)
            else:
                user.roles.append(role)
                
    # replace existing groups with respective db instances
    if user.groups:
        groups=user.groups
        user.groups = []
        for group in groups:
            existing_group = check_object_name(object_type='group', name=group.name)
            if existing_group:
                user.groups.append(existing_group)
            else:
                user.groups.append(group)
                
    return user


# create new user
def create_user(new_user):

    # prepare new user roles and groups lists
    new_user = fill_roles_groups(new_user)

    # write new user to database
    db.session.add(new_user)
    db.session.commit()

    created_user = get_user_by_name(name=new_user.name)

    # return created user object
    return created_user

# update user details: name/email/password/roles/groups
def update_user(changed_user, existing_user):

    # set roles and groups of changed user
    changed_user = fill_roles_groups(changed_user)

    # update existing user
    existing_user.name = changed_user.name
    existing_user.email = changed_user.email
    # set old password if not changed
    if changed_user.password is None:
        changed_user.password = existing_user.password
    # update roles and groups    
    if changed_user.roles:
        existing_user.roles.extend(changed_user.roles)
    if changed_user.groups:
        existing_user.groups.extend(changed_user.groups)

    # save changes to db
    db.session.commit()

    updated_user = get_user_by_name(name=existing_user.name)

    # return updated user
    return updated_user
