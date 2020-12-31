from flask import Blueprint, redirect
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView

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
    edit_model = True
    

@settings.route("/settings")
@authorize.in_group('admins')
def manage_settings():
    return redirect('/admin/')



