"""Navigation bars setup and helpers"""
from flask import Blueprint, render_template, url_for
from flask_login import current_user

from photoric.config.models import db, Navbar, NavbarItem, Menu, MenuItem
from photoric.modules.core.auth.auth import authorize

# Blueprint initialization
nav = Blueprint(
    'nav', __name__,
    template_folder='templates',
    static_folder='static',
    static_url_path='/static',
    url_prefix='/nav'
)


""" initialize custom context processors and variables to use in templates"""


@nav.app_context_processor
def navbar_processors():
    def list_navbars():
        """ get a list of navbars available """
        return Navbar.query.all()

    def list_navbar_items(navbar_id):
        """ get a list of navbars available """
        return NavbarItem.query.filter_by(navbar_id=navbar_id).all()

    def get_navbar_item_by_id(item_id):
        """ get NavbarItem object """
        return NavbarItem.query.filter_by(id=item_id).first()
    
    def check_navbar_item(item_id):
        """ check visibility and permissions of navbar item """
        item = get_navbar_item_by_id(item_id)
        return (item.visible and
                (not item.anonym_only or not current_user.is_authenticated) and
                (not item.auth_req or current_user.is_authenticated) and
                (item.group_req is None or authorize.in_group(item.group_req)) and
                (item.role_req is None or authorize.has_role(item.role_req)))

    def get_menu_by_name(name):
        """ get MenuItem object """
        return Menu.query.filter_by(name=name).first()

    def check_menu_item(item_id):
        """ check visibility and permissions of menu item """
        item = MenuItem.query.filter_by(id=item_id).first()
        return (item.visible and
                (not item.anonym_only or not current_user.is_authenticated) and
                (not item.auth_req or current_user.is_authenticated) and
                (item.group_req is None or authorize.in_group(item.group_req)) and
                (item.role_req is None or authorize.has_role(item.role_req)))

    return dict(list_navbars=list_navbars,
                list_navbar_items=list_navbar_items,
                get_navbar_item_by_id=get_navbar_item_by_id,
                check_navbar_item=check_navbar_item,
                get_menu_by_name=get_menu_by_name,
                check_menu_item=check_menu_item
                )
