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
            name = 'topbar',
            html_class = 'navbar navbar-expand-sm'
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
            html_class = 'justify-content-end',
        )
        # create topmenu items
        topmenu.items = [
            MenuItem(
                name = 'home',
                desc = 'Go to home page',
                item_target = 'index',
                icon_type = 'svg',
                icon_src = 'house-door'
            ),
            MenuItem(
                item_type = 'dropdown'
                name = 'account',
                desc = 'Account management',
                icon_type = 'svg',
                icon_src = 'person-square'
            )
        ]

        account.children = [
            MenuItem(
                name = 'profile',
                desc = 'Look/edit your profile',
                item_target = 'userconfig.profile',
                auth_req = True
            ),     
            MenuItem(
                name = 'sign up',
                desc = 'Sign Up to get access to all functions',
                item_target = 'auth.signup',
                anonym_only = True
            ),
            MenuItem(
                name = 'sign in',
                desc = 'Sign in to your account',
                item_target = 'auth.signin',
                anonym_only = True
            ),
            MenuItem(
                name = 'sign out',
                desc = 'Sign out from your account',
                item_target = 'auth.logout',
                auth_req = True
            )
        ]

        # create main navbar
        mainnavbar = Navbar(
            name = 'mainbar',
            html_class = 'navbar navbar-expand-sm bg-light navbar-light'
        )
        # create main navbar items
        mainnavbar.items = [
            NavbarItem(
                name = 'collapse_toggle_button',
                item_type = 'button',
            ),
            NavbarItem(
                name = 'mainmenu',
                item_type = 'menu',
            )
        ]
        # create main menu
        mainmenu = Menu(
            name = 'mainmenu',
            html_class='collapse navbar-collapse justify-content-end'
        )
        # create mainmenu items
        mainmenu.items = [
            MenuItem(
                name = 'about',
                desc = 'Read about me and this web-site',
                item_target = 'views.about'
            ),
            MenuItem(
                name = 'galleries',
                desc = 'Look through photo galleries',
                item_target = 'views.galleries'
            ),
            MenuItem(
                name = 'upload',
                desc = 'Upload images',
                item_target = 'files.upload',
                icon_type = 'svg',
                icon_src = 'upload',
                auth_reg = True,
                group_reg = 'contributor'
            ),
            MenuItem(
                name = 'settings',
                desc = 'Configure site behavior',
                item_target = 'admin.settings',
                icon_type = 'svg',
                icon_src = 'gear',
                auth_reg = True,
                group_reg = 'admin'
            ),
            MenuItem(
                name = 'contact',
                desc = 'Contact form',
                item_target = 'views.contact',
                icon_type = 'svg',
                icon_src = 'envelope',
                auth_reg = True
            )
        ]
        # create action navbar
        actionnavbar = Navbar(
            name = 'actionbar',
            html_class = 'navbar navbar-expand-sm'
            html_style='display:none;'
        )
        # create action navbar items
        actionnavbar.items = [
            NavbarItem(
                name = 'actionmenu',
                item_type = 'menu'
            )
        ]
        # create action menu
        actionmenu = Menu(
            name = 'actionmenu',
            html_class='justify-content-end'
        )
        # create actionmenu items
        actionmenu.items = [
            MenuItem(
                name = 'share',
                desc = 'Share selected albums/images',
                item_target = 'views.about'
            ),
            MenuItem(
                name = 'galleries',
                desc = 'Look through photo galleries',
                item_target = 'views.galleries'
            ),
            MenuItem(
                name = 'upload',
                desc = 'Upload images',
                item_target = 'files.upload',
                icon_type = 'svg',
                icon_src = 'upload',
                auth_reg = True,
                group_reg = 'contributor'
            ),
            MenuItem(
                name = 'settings',
                desc = 'Configure site behavior',
                item_target = 'admin.settings',
                icon_type = 'svg',
                icon_src = 'gear',
                auth_reg = True,
                group_reg = 'admin'
            ),
            MenuItem(
                name = 'contact',
                desc = 'Contact form',
                item_target = 'views.contact',
                icon_type = 'svg',
                icon_src = 'envelope',
                auth_reg = True
            )
        ]
        
    db.session.add(topnavbar, topmenu, mainnavbar, mainmenu, actionbar)
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
           (not item.anonym_only or not current_user.is_authenticated) and \
                (not item.auth_req or current_user.is_authenticated) and \
                (item.group_req is NULL or item.group_req in current_user.groups) and \
                (item.role_req is NULL or item.role_req in current_user.roles)

@nav.app_context_processor()
def list_navbar_item_templates(id):
    """ return a list of navbar items templates """
    navbar = Navbar.query.filter_by(id = id).first()
    templates = []
    if navbar is not None:
        for item in navbar.items:
            item_template = url_for(
                'nav.templates', filename = '/' + navbar.name + '/' + item.item_src
            )
            templates.append({item, item_template})
    return templates

@nav.app_context_processor()
def get_menu_by_name(name):
    """ get rMenuItem object """
    return Menu.query.filter_by(name = name).first()

@nav.app_context_processor()
def check_menu_item(id):
    """ check viibility and permissions of menu item """
    item = MenuItem.query.filter_by(id = id).first()
    return (item.visible and \
           (not item.anonym_only or not current_user.is_authenticated) and \
            (not item.auth_req or current_user.is_authenticated) and \
            (item.group_req is NULL or item.group_req in current_user.groups) and \
            (item.role_req is NULL or item.role_req in current_user.roles))


@menu.route("/about")
def about():
    return render_template('about.html')

    
