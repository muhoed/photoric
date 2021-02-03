from flask import redirect, request, url_for
from flask_admin.contrib.sqla import ModelView
from wtforms.validators import (
    InputRequired,
    Email,
    Length
)

from photoric.modules.auth.auth import authorize
from photoric import db
from photoric.modules.auth.models import User, Role, Group
from photoric.core.models import Navbar, NavbarItem
from photoric.core.models import Menu, MenuItem, Album, Image, Config
from photoric.modules.admin import admin_bp, admin_manager


# customize flask-admin ModelView to tune its functionality
class PhotoricView(ModelView):
    page_size = 20
    create_modal = True
    edit_modal = True

    def is_accessible(self):
        return authorize.in_group('admins')

    def inaccessible_callback(self, name, **kwargs):
        # redirect to login page if user doesn't have access
        return redirect(url_for('auth.signin', next=request.url))

# create admin views for different models
class UserView(PhotoricView):
    column_exclude_list = ['password']
    column_searchable_list = ['name', 'email']
    column_filters = ['created_on', 'last_login']
    column_editable_list = ['name', 'email']
    form_args = {
        'name': {
            'label': 'Username:',
             'validators': [InputRequired(message='Please enter name'),
                            Length(min=3, message='Name must be at least 3 symbols long')]
        },
        'email': {
            'label': 'E-mail address:',
             'validators': [InputRequired(message='Please enter email address'),
                            Email(
                                message='Please enter valid email address',
                                check_deliverability=True
                            )]
        }
    }


class RoleView(PhotoricView):
    column_searchable_list = ['name']
    column_editable_list = ['name', 'restriction']
    form_args = {
        'name': {
            'label': 'Role name:',
             'validators': [InputRequired(message='Please enter a role name'),
                            Length(min=3, message='Name must be at least 3 symbols long')]
        },
        'email': {
            'label': 'E-mail address:',
             'validators': [InputRequired(message='Please enter email address'),
                            Email(
                                message='Please enter valid email address',
                                check_deliverability=True
                            )]
        }
    }

# register models with admin_manager
admin_manager.add_view(UserView(User, db.session, category='Users and Access rights'))
admin_manager.add_view(PhotoricView(Role, db.session, category='Users and Access rights'))
admin_manager.add_view(PhotoricView(Group, db.session, category='Users and Access rights'))
admin_manager.add_view(PhotoricView(Album, db.session, category='Gallery Items'))
admin_manager.add_view(PhotoricView(Image, db.session, category='Gallery Items'))
admin_manager.add_view(PhotoricView(Navbar, db.session, category='Navigation and Menu system'))
admin_manager.add_view(PhotoricView(NavbarItem, db.session, category='Navigation and Menu system'))
admin_manager.add_view(PhotoricView(Menu, db.session, category='Navigation and Menu system'))
admin_manager.add_view(PhotoricView(MenuItem, db.session, category='Navigation and Menu system'))
admin_manager.add_view(PhotoricView(Config, db.session, category='Style and Behavior'))


@admin_bp.route("/settings")
@authorize.in_group('admins')
def manage_settings():
    return redirect('/admin/')



