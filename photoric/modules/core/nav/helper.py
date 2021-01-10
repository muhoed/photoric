from  photoric.config.models import Navbar, Menu


def get_navbar_by_name(name):
    """ get Navbar object by name """
    return Navbar.query.filter_by(name=name).first()

def get_menu_by_name(name):
        """ get MenuItem object """
        return Menu.query.filter_by(name=name).first()
