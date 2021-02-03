"""Initialize API blueprint"""
from flask import Blueprint
from flask_restful import Api


# Blueprint initialization
api_bp = Blueprint(
    'api', __name__,
    url_prefix='/api/v.1.0',
    template_folder='templates',
    static_folder='static',
    static_url_path='/static'
)


# Initialize API object
api = Api(api_bp)


from photoric.modules.api import users, albums, images
