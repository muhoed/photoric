from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import backref
from datetime import datetime
from flask_login import UserMixin
from flask_authorize import RestrictionsMixin, AllowancesMixin
from flask_authorize import PermissionsMixin
from werkzeug.security import generate_password_hash, check_password_hash


db = SQLAlchemy()

# map tables to classes
UserGroup = db.Table('user_group',
                     db.Column('user_id',
                               db.Integer,
                               db.ForeignKey('users.id')),
                     db.Column('group_id',
                               db.Integer,
                               db.ForeignKey('groups.id'))
)


UserRole = db.Table('user_role',
                    db.Column('user_id',
                              db.Integer,
                              db.ForeignKey('users.id')),
                    db.Column('role_id',
                              db.Integer,
                              db.ForeignKey('roles.id'))
)

# to be revised
# AlbumImage = db.Table('album_image',
#                      db.Column('album_id',
#                                db.Integer,
#                                db.ForeignKey('albums.id')),
#                      db.Column('image_id',
#                                db.Integer,
#                                db.ForeignKey('images.id'))
#)    

# declare models

""" polymorthic relations should be corrected
# base class for gallery items
class GalleryItem(db.Model, PermissionsMixin):
    __tablename__ = 'gallery_items'

    __permissions__ = dict(
        owner=['create', 'read', 'update', 'delete', 'revoke'],
        group=['read', 'update', 'revoke'],
        other=['read']
    )
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(50))
    name = db.Column(db.String(100), unique=True, nullable=True)
    description = db.Column(db.String(500), nullable=True)
    keywords = db.Column(db.String(255), nullable=True)
    is_published = db.Column(db.Boolean(), nullable=False, default=False)
    published_on = db.Column(db.DateTime, nullable=True, index=True)

    __mapper_args__ = {
        'polymorphic_identity': 'gallery_item',
        'polymorphic_on': type,
        'with_polymorphic': '*'
    }

    def publish(self):
        # mark gallery item as published, i.e. accessible for both registered and anonymous users
        is_published = True

    def unpublish(self):
        # mark gallery item as not published, i.e. accessible for both registered and anonymous users
        is_published = False
"""

# class Image(GalleryItem):
class Image(db.Model, PermissionsMixin):
    __tablename__ = "images"

    __permissions__ = dict(
        owner=['create', 'read', 'update', 'delete', 'revoke'],
        group=['read', 'update', 'revoke'],
        other=['read']
    )

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    parent_id=db.Column(db.Integer, db.ForeignKey('albums.id'))
    description = db.Column(db.String(500), nullable=True)
    keywords = db.Column(db.String(255), nullable=True)
    filename = db.Column(db.String, unique=True, nullable=False)
    url = db.Column(db.String(255), nullable=False)
    uploaded_on = db.Column(db.DateTime, nullable=False, default=datetime.now)
    captured_on = db.Column(db.DateTime, nullable=True)
    location = db.Column(db.Text, nullable=True)
    is_published = db.Column(db.Boolean(), nullable=False, default=False)
    published_on = db.Column(db.DateTime, nullable=True, index=True)
    parent_album = db.relationship(
        'Album',
        #secondary=AlbumImage,
        back_populates='children_images')
    
    def publish(self):
        # mark gallery item as published, i.e. accessible for both registered and anonymous users
        is_published = True

    def unpublish(self):
        # mark gallery item as not published, i.e. accessible for both registered and anonymous users
        is_published = False

    def __repr__(self):
        return '<Image %r>' % self.filename

"""
    __mapper_args__ = {
        'polymorphic_identity': 'image',
        'polymorphic_load': 'inline'
    }
"""


# class Album(GalleryItem):
class Album(db.Model, PermissionsMixin):
    __tablename__ = "albums"

    __permissions__ = dict(
        owner=['create', 'read', 'update', 'delete', 'revoke'],
        group=['read', 'update', 'revoke'],
        other=['read']
    )

    id = db.Column(db.Integer, primary_key=True)
    parent_id = db.Column(db.Integer, db.ForeignKey('albums.id'))
    name = db.Column(db.String(100), unique=True, nullable=False)
    description = db.Column(db.String(500), nullable=True)
    keywords = db.Column(db.String(255), nullable=True)
    icon_id = db.Column(db.Integer, nullable=True)
    created_on = db.Column(db.DateTime, nullable=False, default=datetime.now)
    is_published = db.Column(db.Boolean(), nullable=False, default=False)
    published_on = db.Column(db.DateTime, nullable=True, index=True)
    children_images = db.relationship(
        'Image',
        # secondary=AlbumImage,
        back_populates='parent_album'
    )
    children_albums = db.relationship(
        'Album', backref=backref('parent',
        remote_side=[id])
    )

    def publish(self):
        # mark gallery item as published, i.e. accessible for both registered and anonymous users
        is_published = True

    def unpublish(self):
        # mark gallery item as not published, i.e. accessible for both registered and anonymous users
        is_published = False

    def __repr__(self):
        return '<Album %r>' % self.name
"""    
    __mapper_args__ = {
        'polymorphic_identity': 'album',
        'polymorphic_load': 'inline'
    }
"""



class User(UserMixin, db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False, unique=True)
    email = db.Column(db.String, )
    password = db.Column(db.String, nullable=False)
    created_on = db.Column(db.DateTime, nullable=False, default=datetime.now)
    active = db.Column(db.Boolean, nullable=False, default=True)
    last_login = db.Column(db.DateTime, nullable=True)

    roles = db.relationship('Role', secondary=UserRole)
    groups = db.relationship('Group', secondary=UserGroup)

    @property
    def is_authenticated(self):
        return True

    def is_active(self):
    # return True if the user is active (was not banned)
        return self.active

    @property
    def is_anonymous(self):
        return False

    def set_password(self, password):
        """create hashed password"""
        self.password = generate_password_hash(password, method='sha256')

    def check_password(self, password):
        """check hashed password"""
        return check_password_hash(self.password, password)

    def get_id(self):
        return self.id

    # Required for administrative interface
    def __unicode__(self):
        return self.name
    
    def __repr__(self):
        return '<User %r>' % self.name
        

class Group(db.Model, AllowancesMixin):
    __tablename__ = 'groups'

    __allowances__ = {}

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
        

class Role(db.Model, RestrictionsMixin):
    __tablename__='roles'

    __restrictions__ = {}

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    

class Navbar(db.Model):
    __tablename__='navbars'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    html_class = db.Column(db.String(255), nullable=False, default='')
    html_style = db.Column(db.String(255), nullable=False, default='')

    items = db.relationship('NavbarItem', back_populates='navbar') 
    

class NavbarItem(db.Model):
    __tablename__='navbar_items'

    id = db.Column(db.Integer, primary_key=True)
    navbar_id = db.Column(db.Integer, db.ForeignKey('navbars.id'))
    name = db.Column(db.String(100), unique=True, nullable=False)
    item_type = db.Column(db.String(100), nullable=False)
    item_target = db.Column(db.String(255), nullable=True)
    icon_type = db.Column(db.String(50), nullable=True)
    icon_src = db.Column(db.String(255), nullable=True)
    visible = db.Column(db.Boolean, nullable=False, default=True)
    anonym_only = db.Column(db.Boolean, nullable=False, default=False)
    auth_req = db.Column(db.Boolean, nullable=False, default=False)
    group_req = db.Column(db.String(100), nullable=True)
    role_req = db.Column(db.String(100), nullable=True)

    item_src = db.column_property('/' + item_type + '/' + name + '.html')
    
    navbar = db.relationship('Navbar', back_populates='items')


class Menu(db.Model):
    __tablename__='menus'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    html_class = db.Column(db.String(255), nullable=False, default='')
    html_style = db.Column(db.String(255), nullable=False, default='')

    items = db.relationship('MenuItem', back_populates='menu') 

class MenuItem(db.Model):
    __tablename__='menu_items'
    
    id = db.Column(db.Integer, primary_key=True)
    menu_id = db.Column(db.Integer, db.ForeignKey('menus.id'))
    parent_id = db.Column(db.Integer, db.ForeignKey('menu_items.id'))
    item_type = db.Column(db.String(20), default='plain')
    name = db.Column(db.String(100), nullable=False, unique=True)
    desc = db.Column(db.String(255), nullable=False)
    item_target = db.Column(db.String(255), nullable=True)
    icon_type = db.Column(db.String(50), nullable=True)
    icon_src = db.Column(db.String(255), nullable=True)
    visible = db.Column(db.Boolean, nullable=False, default=True)
    anonym_only = db.Column(db.Boolean, nullable=False, default=False)
    auth_req = db.Column(db.Boolean, nullable=False, default=False)
    group_req = db.Column(db.String(100), nullable=True)
    role_req = db.Column(db.String(100), nullable=True)

    menu = db.relationship('Menu', back_populates='items')
    children = db.relationship('MenuItem')
    

class Config(db.Model, PermissionsMixin):
    __tablename__ = "configs"

    __permissions__ = dict(
        owner=['read', 'update', 'delete', 'revoke'],
        group=['read', 'update'],
        other=['read']
    )
    id = db.Column(db.Integer, primary_key=True)
    theme = db.Column(db.String, nullable=False, default='light')
    view_mode = db.Column(db.String, nullable=False, default='grid')


models = {
    'album':Album,
    'image':Image,
    'user':User,
    'role':Role,
    'group':Group,
    'navbar':Navbar,
    'navbar_item':NavbarItem,
    'menu':Menu,
    'menu_item':MenuItem
    }

def check_object_name(object_type=None, name=None):
    if object_type is None or name is None:
        return False
    requested_object = db.session.query(models[object_type]).filter_by(name=name).first()
    if requested_object:
        return True
    return False
