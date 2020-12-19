from flask import Blueprint


from photoric.config.models import User, Role, Group
from photoric.modules.core.helpers.database.db import get_gallery_items, get_user_by_name


before_after = Blueprint('before_after', __name__)

@before_after.before_app_first_request():
def initial_setup():
    """ create admin user if not exist """
    if get_user_by_name('admin') is None:
        # create administrator role
        admin_role = Role(
            name='admin',
            allowances= '*'
        )
        # create administrators group
        admins_group = Group(
            name='admins'
        )
        # create contributors group
        contributors_group = Group(
            name='contributors',
            restrictions = dict(
                gallery_items=['delete'],
                albums=['delete'],
                images=['delete']
            )
        )
        # create user and map it to respective group annd role
        admin_user = User(name='admin', password=set_password('admin'))
        admin_user.roles = [admin_role]
        admin_user.groups = [admins_group, contributors_group]
        
        # insert new user, its role and group to to database
        db.session.add(admin_role, admins_group, contributors_group, admin_user)
        db.session.commit()
