"""Routes for functions accessible from action menu"""
from flask import Blueprint, render_template

# Blueprint initialization
menu = Blueprint(
    'menu', __name__,
    template_folder='templates',
    static_folder='static'
)

@menu.route("/about")
def about():
    return render_template('about.html')

    
