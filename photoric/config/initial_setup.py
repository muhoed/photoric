from photoric.config.models import db, User, Role, Group, Navbar, NavbarItem
from photoric.config.models import Menu, MenuItem, Album, Image, Config
from photoric.modules.core.auth.helper import get_user_by_name
from photoric.modules.core.nav.helper import get_navbar_by_name, get_menu_by_name
from photoric.modules.core.admin.settings import admin_manager, PhotoricView

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
    if get_navbar_by_name('topbar') is None:
        # create top navbar
        topnavbar = Navbar(
            name='topbar',
            html_class='navbar navbar-expand pt-1 pb-1'
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
                name='topmenu',
                item_type='menu'
            ),
            NavbarItem(
                name='simple_search',
                item_type='form',
                item_target='search.simple_search'
            )
        ]

        db.session.add(topnavbar)
        db.session.commit()

        if get_menu_by_name('topmenu') is None:
            # create top menu
            topmenu = Menu(
                name='topmenu',
                html_class='navbar-nav'
            )
            # create topmenu items
            topmenu.items = [
                MenuItem(
                    name='home',
                    desc='Go to home page',
                    item_target='views.index',
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
                            item_target='views.index',
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

            db.session.add(topmenu)
            db.session.commit()

        if get_navbar_by_name('mainbar') is None:
            # create main navbar
            mainnavbar = Navbar(
                name='mainbar',
                html_class='navbar navbar-expand-sm pt-0 pb-0 bg-light navbar-light d-flex border border-left-0 border-right-0 border-success',
            )
            # create main navbar items
            mainnavbar.items = [
                NavbarItem(
                    name='collapse_toggle_button',
                    item_type='button',
                    item_target='mainmenu'
                ),
                NavbarItem(
                    name='mainmenu',
                    item_type='menu',
                ),
                NavbarItem(
                    name='upload_button',
                    item_type='button',
                    item_target='#',
                    icon_type='svg',
                    icon_src='upload',
                    auth_req=True,
                    group_req='contributors'
                ),
                NavbarItem(
                    name='create_album_button',
                    item_type='button',
                    item_target='#create_album',
                    icon_type='svg',
                    icon_src='folder-plus',
                    auth_req=True,
                    group_req='contributors'
                ),
                NavbarItem(
                    name='settings_button',
                    item_type='button',
                    item_target='settings.manage_settings',
                    icon_type='svg',
                    icon_src='gear',
                    auth_req=True,
                    group_req='admins'
                )
            ]

            db.session.add(mainnavbar)
            db.session.commit()

            if get_menu_by_name('mainmenu') is None:
                # create first part of main menu
                mainmenu = Menu(
                    name='mainmenu',
                    html_class='collapse navbar-collapse flex-grow-1 font-weight-bold'
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
                        item_target='views.index'
                    ),
                    MenuItem(
                        name='contact',
                        desc='Contact form',
                        item_target='views.index',
                        auth_req=True
                    )
                ]

                db.session.add(mainmenu)
                db.session.commit()
        

        if get_navbar_by_name('actionbar') is None:
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

            db.session.add(actionnavbar)
            db.session.commit()

            if get_menu_by_name('actionmenu') is None:
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
                        item_target='views.index',
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
                                item_target='views.index',
                                auth_req=True,
                                group_req='contributors'
                            ),
                            MenuItem(
                                name='remove',
                                desc='Remove images / albums from an album',
                                item_target='views.index',
                                auth_req=True,
                                group_req='contributors'
                            ),
                            MenuItem(
                                name='set',
                                desc='Set an image as an album icon',
                                item_target='views.index',
                                auth_req=True,
                                group_req='contributors'
                            )
                        ]
                    ),
                    MenuItem(
                        name='download',
                        desc='Download images / albums',
                        item_target='views.index',
                        icon_type='svg',
                        icon_src='download',
                        auth_req=True,
                        group_req='private'
                    ),
                    MenuItem(
                        name='delete',
                        desc='Delete images / albums',
                        item_target='views.index',
                        icon_type='svg',
                        icon_src='trash',
                        auth_req=True,
                        group_req='admins',
                        role_req='admin'
                    )
                ]
                
                db.session.add(actionmenu)
                db.session.commit()

        if get_navbar_by_name('sidebar') is None:
            # create side navbar
            sidenavbar = Navbar(
                name='sidebar',
                html_class='navbar navbar-light d-none d-md-flex flex-column',
                html_style='min-width:8%;'
            )
            # create side navbar items
            sidenavbar.items = [
                NavbarItem(
                    name='sidemenu',
                    item_type='menu'
                )
            ]

            db.session.add(sidenavbar)
            db.session.commit()

            if get_menu_by_name('sidemenu') is None:
                # create action menu
                sidemenu = Menu(
                    name='sidemenu',
                    html_class='navbar-nav align-self-start font-weight-bold',
                )
                # create sidemenu items
                sidemenu.items = [

                    MenuItem(
                        item_type='tree',
                        name='albums',
                        desc='Albums tree',
                        item_target='albumsTree'
                    ),
                    MenuItem(
                        name='images',
                        desc='Images not included in albums',
                        item_target='views.index'
                    ),
                    MenuItem(
                        item_type='tree',
                        name='shares',
                        desc='Shared items tree',
                        item_target='sharesTree'
                    )
                ]

                db.session.add(sidemenu)
                db.session.commit()

    # register models with admin_manager
    admin_manager.add_view(PhotoricView(User, db.session, category='Users and Access rights'))
    admin_manager.add_view(PhotoricView(Role, db.session, category='Users and Access rights'))
    admin_manager.add_view(PhotoricView(Group, db.session, category='Users and Access rights'))
    admin_manager.add_view(PhotoricView(Album, db.session, category='Gallery Items'))
    admin_manager.add_view(PhotoricView(Image, db.session, category='Gallery Items'))
    admin_manager.add_view(PhotoricView(Navbar, db.session, category='Navigation and Menu system'))
    admin_manager.add_view(PhotoricView(NavbarItem, db.session, category='Navigation and Menu system'))
    admin_manager.add_view(PhotoricView(Menu, db.session, category='Navigation and Menu system'))
    admin_manager.add_view(PhotoricView(MenuItem, db.session, category='Navigation and Menu system'))
    admin_manager.add_view(PhotoricView(Config, db.session, category='Style and Behavior'))
