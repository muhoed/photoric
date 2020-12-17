from flask_sqlalchemy import SQLAlchemy

from photoric.config.models import Menu, Navbar
from photoric.modules.core.helpers.form.forms import SimpleSearch

def processors():
    """ initialize custom templates context processors """

    def get_navbars():
        """ get a list of navbars available """
        return Navbar.query.all()

    def get_menu_item(name):
        """ get respective menu from database """
        return Menu.query.filter_by(name = name).first()

    def simple_search():
        """ inflect search form to templates """
        return dict(search_form=SimpleSearch())

    return dict(
        get_navbars =  get_navbars,
        get_menu_item = get_menu,
        simple_search = simple_search
    )
