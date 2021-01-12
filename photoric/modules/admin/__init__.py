"""admin dashboard module""" 
from flask import Blueprint
from flask_admin import Admin


# Initialize administration blueprint
admin_bp = Blueprint('settings', __name__,
                     template_folder="templates",
                     static_folder="static",
                     url_prefix='/settings',
                     static_url_path='/settings/static')

# Initialize admin_manager object
admin_manager = Admin(name='Settings',
                      template_mode='bootstrap4',
                      base_template='settings_base.html')


from photoric.modules.admin import admin
