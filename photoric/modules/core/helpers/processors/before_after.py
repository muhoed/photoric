from flask import Blueprint


from photoric.config.models import User, Role, Group
from photoric.modules.core.helpers.database.db import get_gallery_items, get_user_by_name


before_after = Blueprint('before_after', __name__)

@before_after.before_app_first_request():
def initial_setup():
    """ create admin user if not exist """
    if get_user_by_name('admin') is None:
        # create administrator role
        role = Role(
            name='admin',
            allowances=dict(
                gallery_items = ['create', 'update', 'read', 'delete', 'revoke'],
                albums = ['create', 'update', 'read', 'delete', 'revoke'],
                images = ['create', 'update', 'read', 'delete', 'revoke'],
                menu = ['create', 'update', 'read', 'delete', 'revoke'],
                configs = ['create', 'update', 'read', 'delete', 'revoke']
            )
        )
        # create administrators group
        group = Group(
            name='admins',
            restrictions=dict(
                gallery_items = ['create', 'delete'],
                albums = ['create', 'delete'],
                images = [['create', 'delete'],
                menu = ['create', 'delete'],
                configs = ['create', 'delete']
            )
        )
        # create user and map it to respective group annd role
        admin = User(name='admin', password=set_password('admin'))
        admin.roles = [role]
        admin.groups = [group]

    """ create base navigation elements """
    if get_navbars() is None:
        # create top navbar
        topnavbar = Navbar(
            name = 'topmenu'
        )
        # create top navbar items
        topnavbar.items = [
            NavbarItem(
                name = 'site_logo',
                item_type = 'logo',
                item_target = '/',
                icon_type = 'favicon',
                icon_source = 'favicon.ico'
                auth_req = False
            ),
            NavbarItem(
                name = 'search',
                item_type = 'logo',
                item_source = 
                item_target = '/',
                auth_req = False,
                role_req
        
        # insert new user, its role and group to to database
        db.session.add(role, group, admin, )
        db.session.commit()
