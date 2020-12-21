"""Navigation bars setup and helpers"""
from flask import Blueprint, render_template, url_for
from flask_login import current_user

from photoric.config.models import db, Navbar, NavbarItem, Menu, MenuItem

# Blueprint initialization
nav = Blueprint(
    'nav', __name__,
    template_folder='templates',
    static_folder='static',
    url_prefix='/nav'
)


""" initialize custom templates context processors """


@nav.app_context_processor
def navbar_processors():
    def list_navbars():
        """ get a list of navbars available """
        return Navbar.query.all()

    def get_navbar_item_by_id(item_id):
        """ get NavbarItem object """
        return NavbarItem.query.filter_by(id=item_id).first()
    
    def check_navbar_item(item_id):
        """ check visibility and permissions of navbar item """
        item = get_navbar_item_by_id(item_id)
        return (item.visible and
                (not item.anonym_only or not current_user.is_authenticated) and
                (not item.auth_req or current_user.is_authenticated) and
                (item.group_req is None or item.group_req in current_user.groups) and
                (item.role_req is None or item.role_req in current_user.roles))

    def list_navbar_item_templates(item_id):
        """ return a list of navbar items templates """
        navbar = Navbar.query.filter_by(id=item_id).first()
        templates = []
        if navbar is not None:
            for item in navbar.items:
                item_template = '/nav/' + navbar.name + '/' + item.item_src
                templates.append({item.id, item_template})
        return templates

    def get_menu_by_name(name):
        """ get MenuItem object """
        return Menu.query.filter_by(name=name).first()

    def check_menu_item(item_id):
        """ check visibility and permissions of menu item """
        item = MenuItem.query.filter_by(id=item_id).first()
        return (item.visible and
                (not item.anonym_only or not current_user.is_authenticated) and
                (not item.auth_req or current_user.is_authenticated) and
                (item.group_req is None or item.group_req in current_user.groups) and
                (item.role_req is None or item.role_req in current_user.roles))

    return dict(list_navbars=list_navbars,
                get_navbar_item_by_id=get_navbar_item_by_id,
                check_navbar_item=check_navbar_item,
                list_navbar_item_templates=list_navbar_item_templates,
                get_menu_by_name=get_menu_by_name,
                check_menu_item=check_menu_item
                )


""" view routes """


@nav.route("/about")
def about():
    return render_template('about.html')
