from flask import Blueprint, redirect, request, url_for
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from wtforms.validators import (
    InputRequired,
    Email,
    Length
)

from photoric.modules.core.auth.auth import authorize


settings = Blueprint('settings', __name__,
                     template_folder="templates",
                     static_folder="static",
                     url_prefix='/settings',
                     static_url_path='/settings/static')

admin_manager = Admin(name='Settings',
                      template_mode='bootstrap4',
                      base_template='settings_base.html')


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


@settings.route("/settings")
@authorize.in_group('admins')
def manage_settings():
    return redirect('/admin/')



