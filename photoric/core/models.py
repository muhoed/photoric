from sqlalchemy.orm import backref
from datetime import datetime
from flask_authorize import RestrictionsMixin, AllowancesMixin, PermissionsMixin

from photoric import db
from photoric.core.mixins import PhotoricMixin
from photoric.modules.auth.models import User


# map tables to classes
AlbumImage = db.Table('album_image',
                      db.Column('album_id',
                                db.Integer,
                                db.ForeignKey('albums.id')),
                      db.Column('image_id',
                                db.Integer,
                                db.ForeignKey('images.id'))
)    


# declare models

# class Image(GalleryItem):
class Image(db.Model, PermissionsMixin):
    __tablename__ = "images"

    __user_model__ = User
    __permissions__ = dict(
        owner=['create', 'read', 'update', 'delete', 'revoke'],
        group=['read', 'update', 'revoke'],
        other=['read']
    )

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    # parent_id=db.Column(db.Integer, db.ForeignKey('albums.id'))
    description = db.Column(db.String(500), nullable=True)
    keywords = db.Column(db.String(255), nullable=True)
    filename = db.Column(db.String, unique=True, nullable=False)
    url = db.Column(db.String(255), nullable=False)
    uploaded_on = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    captured_on = db.Column(db.DateTime, nullable=True)
    location = db.Column(db.Text, nullable=True)
    is_published = db.Column(db.Boolean(), nullable=False, default=False)
    published_on = db.Column(db.DateTime, nullable=True, index=True)
    parent_albums = db.relationship(
        'Album',
        secondary=AlbumImage,
        back_populates='children_images')
    
    def publish(self):
        # mark gallery item as published, i.e. accessible for both registered and anonymous users
        is_published = True

    def unpublish(self):
        # mark gallery item as not published, i.e. accessible for both registered and anonymous users
        is_published = False

    def __repr__(self):
        return '<Image %r>' % self.filename


# class Album(GalleryItem):
class Album(db.Model, PermissionsMixin):
    __tablename__ = "albums"

    __user_model__ = User
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
        secondary=AlbumImage,
        back_populates='parent_albums'
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
