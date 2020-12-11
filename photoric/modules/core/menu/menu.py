"""Routes for functions accessible from action menu"""
from flask import Blueprint

# Blueprint initialization
menu = Blueprint(
    'menu', __name__,
    template_folder='templates',
    static_folder='static'
)


