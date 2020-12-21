from photoric.config.models import db, User, Role, Group, Navbar, NavbarItem, Menu, MenuItem
from photoric.modules.core.auth.helper import get_user_by_name

def initial_setup():
    """ create admin user if not exist """
    if get_user_by_name('admin') is None:

        # create user and map it to respective groups and role
        admin_user = User(name='admin')
        admin_user.set_password('admin')
        admin_user.roles = [
            Role(
                name='admin',
                restrictions={}
            )
        ]
        admin_user.groups = [
            Group(
                name='admins',
                allowances='*'
            ),
            Group(
                name='private',
                allowances=dict(
                    gallery_items=['read'],
                    albums=['read'],
                    images=['read']
                )
            ),
            Group(
                name='contributors',
                allowances=dict(
                    gallery_items=['read', 'create', 'update', 'revoke'],
                    albums=['read', 'create', 'update', 'revoke'],
                    images=['read', 'create', 'update', 'revoke']
                )
            )
        ]

        db.session.add(admin_user)
        db.session.commit()
        
    """ create base navigation elements """
    navbars = Navbar.query.first()
    if navbars is None:
        # create top navbar
        topnavbar = Navbar(
            name='topbar',
            html_class='navbar navbar-expand-sm'
        )
        # create top navbar items
        topnavbar.items = [
            NavbarItem(
                name='site_logo',
                item_type='logo',
                item_target='views.index',
                icon_type='favicon',
                icon_src='favicon.ico'
            ),
            NavbarItem(
                name='simple_search',
                item_type='form',
                item_target='search.simple_search'
            ),
            NavbarItem(
                name='topmenu',
                item_type='menu'
            )
        ]
        # create top menu
        topmenu = Menu(
            name='topmenu',
            html_class='justify-content-end'
        )
        # create topmenu items
        topmenu.items = [
            MenuItem(
                name='home',
                desc='Go to home page',
                item_target='index',
                icon_type='svg',
                icon_src='house-door'
            ),
            MenuItem(
                item_type='dropdown',
                name='account',
                desc='Account management',
                icon_type='svg',
                icon_src='person-square',
                children=[
                    MenuItem(
                        name='profile',
                        desc='Look/edit your profile',
                        item_target='userconfig.profile',
                        auth_req=True
                    ),
                    MenuItem(
                        name='sign up',
                        desc='Sign Up to get access to all functions',
                        item_target='auth.signup',
                        anonym_only=True
                    ),
                    MenuItem(
                        name='sign in',
                        desc='Sign in to your account',
                        item_target='auth.signin',
                        anonym_only=True
                    ),
                    MenuItem(
                        name='sign out',
                        desc='Sign out from your account',
                        item_target='auth.logout',
                        auth_req=True
                    )
                ]
            )
        ]

        db.session.add(topnavbar, topmenu)
        db.session.commit()

        # create main navbar
        mainnavbar = Navbar(
            name='mainbar',
            html_class='navbar navbar-expand-sm bg-light navbar-light'
        )
        # create main navbar items
        mainnavbar.items = [
            NavbarItem(
                name='collapse_toggle_button',
                item_type='button',
            ),
            NavbarItem(
                name='mainmenu',
                item_type='menu',
            )
        ]
        # create main menu
        mainmenu = Menu(
            name='mainmenu',
            html_class='collapse navbar-collapse justify-content-end'
        )
        # create mainmenu items
        mainmenu.items = [
            MenuItem(
                name='about',
                desc='Read about me and this web-site',
                item_target='views.about'
            ),
            MenuItem(
                name='galleries',
                desc='Look through photo galleries',
                item_target='views.galleries'
            ),
            MenuItem(
                name='upload',
                desc='Upload images',
                item_target='files.upload',
                icon_type='svg',
                icon_src='upload',
                auth_req=True,
                group_req='contributor'
            ),
            MenuItem(
                name='settings',
                desc='Configure site behavior',
                item_target='admin.settings',
                icon_type='svg',
                icon_src='gear',
                auth_req=True,
                group_req='admin'
            ),
            MenuItem(
                name='contact',
                desc='Contact form',
                item_target='views.contact',
                icon_type='svg',
                icon_src='envelope',
                auth_req=True
            )
        ]

        db.session.add(mainnavbar, mainmenu)
        db.session.commit()
        
        # create action navbar
        actionnavbar = Navbar(
            name='actionbar',
            html_class='navbar navbar-expand-sm',
            html_style='display:none;'
        )
        # create action navbar items
        actionnavbar.items = [
            NavbarItem(
                name='actionmenu',
                item_type='menu'
            )
        ]
        # create action menu
        actionmenu = Menu(
            name='actionmenu',
            html_class='justify-content-end',
        )
        # create actionmenu items
        actionmenu.items = [
            MenuItem(
                name='share',
                desc='Share selected albums/images',
                item_target='share.share',
                icon_type='svg',
                icon_src='share',
                auth_req=True
            ),
            MenuItem(
                item_type='dropdown',
                name='album',
                desc='Manage album',
                icon_type='svg',
                icon_src='book',
                group_req='contributors',
                children=[
                    MenuItem(
                        name='add',
                        desc='Add images / albums to a new or existing album',
                        item_target='albums.insert',
                        auth_req=True,
                        group_req='contributors'
                    ),
                    MenuItem(
                        name='remove',
                        desc='Remove images / albums from an album',
                        item_target='albums.remove',
                        auth_req=True,
                        group_req='contributors'
                    ),
                    MenuItem(
                        name='set',
                        desc='Set an image as an album icon',
                        item_target='albums.icon',
                        auth_req=True,
                        group_req='contributors'
                    )
                ]
            ),
            MenuItem(
                name='download',
                desc='Download images / albums',
                item_target='files.download',
                icon_type='svg',
                icon_src='download',
                auth_req=True,
                group_req='private'
            ),
            MenuItem(
                name='delete',
                desc='Delete images / albums',
                item_target='files.delete',
                icon_type='svg',
                icon_src='trash',
                auth_req=True,
                group_req='admins',
                role_req='admin'
            )
        ]
        
        db.session.add(actionnavbar, actionmenu)
        db.session.commit()
