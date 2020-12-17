"""Navigation bars setup and helpers"""
from flask import Blueprint, render_template
from flask_login import current_user

from photoric.config.models import Navbar, NavbarItem, Menu, MenuItem

# Blueprint initialization
nav = Blueprint(
    'nav', __name__,
    template_folder='templates',
    static_folder='static'
)

@nav.before_app_first_request():
def nav_initial_setup():
    """ create base navigation elements """
    if get_navbars() is None:
        # create top navbar
        topnavbar = Navbar(
            name = 'topbar'
        )
        # create top navbar items
        topnavbar.items = [
            NavbarItem(
                name = 'site_logo',
                item_type = 'logo',
                item_target = 'index',
                icon_type = 'favicon',
                icon_src = 'favicon.ico'
            ),
            NavbarItem(
                name = 'simple_search',
                item_type = 'form',
                item_target = 'search.simple_search'
            ),
            NavbarItem(
                name = 'topmenu',
                item_type = 'menu'
            )
        ]
        # create top menu
        topmenu = Menu(
            name = 'topmenu'
        )
        # create topmenu items
        topmenu.items = [
            MenuItem(
                name = 'home',
                desc = 'Go to home page',
                item_target = 'index',
                icon_type = '',
                icon_src = ''
            ),
            MenuItem(
                name = ,
                desc = ,
                item_target = ,
                icon_type = ,
                icon_src =
            )
        ]


    db.session.add(topnavbar, topmenu)
    db.session.commit()
                
                

""" initialize custom templates context processors """
@nav.app_context_processor()
def list_navbars():
    """ get a list of navbars available """
    return Navbar.query.all()

@nav.app_context_processor()
def get_navbar_item_by_id(id):
    """ get NavbarItem object """
    return NavbarItem.query.filter_by(id = id).first()

@nav.app_context_processor()
def check_navbar_item(id):
    """ check viibility and permissions of navbar item """
    item = get_navbar_item_by_id(id)
    return item.visible and \
                (not item.auth_req or current_user.is_authenticated) and \
                (item.role_req is NULL or item.role_req in current_user.roles)

@nav.app_context_processor()
def get_menu_item_by_id(id):
    """ get rMenuItem object """
    return MenuItem.query.filter_by(id = id).first()

@nav.app_context_processor()
def check_menu_item(id):
    """ check viibility and permissions of menu item """
    item = get_menu_item_by_id(id)
    return item.visible and \
                (not item.auth_req or current_user.is_authenticated) and \
                (item.role_req is NULL or item.role_req in current_user.roles)

@nav.app_context_processor()
def list_navbar_templates():
    """ return a list of navbars templates """
    navbars = list_navbars()
    templates = []
    if navbars is not None:
        for navbar in navbars:
            navbar_template = url_for(
                'nav.templates', filename = '/' + navbar.name + '/' + navbar.name + '.html'
            )
            templates.append([navbar.id, navbar_template])
    return templates

@nav.app_context_processor()
def list_navbar_item_templates(id):
    """ return a list of navbar items templates """
    navbar = Navbar.query.filter_by(id = id).first()
    templates = []
    if navbar is not None:
        for item in navbar.items:
            item_template = url_for(
                'nav.templates', filename = '/' + navbar.name + '/items' + item.src
            )
            templates.append([item.id, item_template])
    return templates

@menu.route("/about")
def about():
    return render_template('about.html')

    
