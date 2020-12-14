from flask import Blueprint, session, render_template, request, url_for, flash
from flask_login import current_user

from photoric.config.models import User, Role, Group
from photoric.modules.core.helpers.database.db import get_gallery_items, get_user_by_name

itemviews = Blueprint('itemviews', __name__, url_prefix='/')

@itemviews.before_first_request():
def initial_setup():
    # create admin user if not exist
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
        # create administrators grup
        group = Group(
            name='admins',
            restrictions=dict(
                gallery_items = ['create', 'delete', 'revoke'],
                albums = ['create', 'delete', 'revoke'],
                images = [['create', 'delete', 'revoke'],
                menu = ['create', 'delete', 'revoke'],
                configs = ['create', 'delete', 'revoke']
            )
        )
        # create user and map it to respective group annd role
        admin = User(name='admin', password=set_password('admin'))
        admin.roles = [role]
        admin.groups = [group]
        # insert new user, its role and group to to database
        db.session.add(role, group, admin)
        db.session.commit()
            

@itemviews.route("/", methods=['GET', 'POST'])
@itemviews.route("/index", methods=['GET', 'POST'])
def index():
    """Show main page"""

    # page was loaded after some actions performed
    if request.method == "POST":
        return TODO

    # page was loaded without action
    else:
        # get top-level gallery items from database
        gallery_items = get_gallery_items('no', '')

        # if user is not admin show gallery items if any
        return render_template('index.html', gallery_items = gallery_items)

        # if user is admin gallery_items is not None load admin version of the page

        # if user is admin and get view items is None load dropzone page to upload

    
            
    
