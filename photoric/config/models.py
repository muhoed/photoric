from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_login import UserMixin, LoginManager
from flask_authorize import RestrictionsMixin, AllowancesMixin
from flask_authorize import PermissionsMixin
from werkzeug.security import generate_password_hash, check_password_hash


db = SQLAlchemy()
login_manager = LoginManager()

# map tables to classes
users_groups = db.Table('users_groups',
    db.Column('user_id',
              db.Integer,
              db.ForeignKey('users.id')),
    db.Column('group_id',
              db.Integer,
              db.ForeignKey('groups.id'))
)


users_roles = db.Table('users_roles',
    db.Column('user_id',
              db.Integer,
              db.ForeignKey('users.id')),
    db.Column('role_id',
              db.Integer,
              db.ForeignKey('roles.id'))
)


albums_images = db.Table('albums_images',
    db.Column('album_id',
              db.Integer,
              db.ForeignKey('albums.id')),
    db.Column('image_id',
              db.Integer,
              db.ForeignKey('images.id'))
)    

# declare models    

# base class for gallery items
class GalleryItems(db.Model, PermissionsMixin):
    __tablename__='gallery_item'
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(50))
    name = db.Column(db.String(100), unique=True, nullable=True)
    description = db.Column(db.String(500), nullable=True)
    keywords = db.Column(db.String(255), nullable=True)
    created_on = db.Column(db.DateTime, nullable=False, default=datetime.now)
    published = db.Column(db.Boolean(), nullable=False, default=False)
    published_on = db.Column(db.DateTime, nullable=True)

    __mapper_args__ = {
        'polymorphic_identity':'gallery_item',
        'polymorphic_on':type
    }
    

class Images(GalleryItems):
    __tablename__="images"
    id = db.Column(db.Integer, db.ForeignKey('gallery_item.id'), primary_key=True)
    filename = db.Column(db.String, unique=True, nullable=False)
    uploaded_on = db.Column(db.DateTime, nullable=False, default=datetime.now)
    location = db.Column(db.String, nullable=True)
    parent = db.relationship(
        'Albums',
        secondary=albums_images,
        back_populates='children_images')

    __mapper_args__ = {
        'polymorphic_identity':'images'
    }
    
    def __repr__(self):
        return '<Image %r>' % self.filename
    

class Albums(GalleryItems):
    __tablename__="albums"
    id = db.Column(db.Integer, db.ForeignKey('gallery_item.id'), primary_key=True)
    parent_id = db.Column(db.Integer, db.ForeignKey('albums.id'))
    icon = db.Column(db.String, nullable=False)                                      
    children_images = db.relationship(
        'Images',
        secondary=albums_images,
        back_populates='parent')
    children_albums = db.relationship(
        'Albums', backref=db.backref('parent', remote_side=[id]))
    
    __mapper_args__ = {
        'polymorphic_identity':'albums'
    }

    def __repr__(self):
        return '<Album %r>' % self.name
        

class Users(UserMixin, db.Model):
    __tablename__="users"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False, unique=True)
    email = db.Column(db.String, nullable=False)
    password = db.Column(db.String, nullable=False)
    created_on = db.Column(db.DateTime, nullable=False, default=datetime.now)
    lasl_login = db.Column(db.DateTime, nullable=True)

    roles = db.relationship('Roles', secondary=users_roles)
    groups = db.relationship('Groups', secondary=users_groups)

    def set_password(self, password):
        """create hashed password"""
        self.password = generate_password_hash(password, method='sha256')

    def check_password(self, password):
        """check hashed password"""
        return check_password_hash(self.password, password)
    
    def __repr__(self):
        return '<User %>' % self.name
        

class Groups(db.Model, RestrictionsMixin):
    __tablename__='groups'                             
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
        

class Roles(db.Model, RestrictionsMixin):
    __tablename__='roles'                             
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)

"""
class MainMenu(db.Model, PermissionsMixin):
    __tablename__='main_menu'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    icon_url = db.Column(db.String(255), nullable=True)
    target_url = db.Column(db.String(255), nullable=False)

class ActionMenu(db.Model, PermissionsMixin):
    __tablename__='action_menu'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    icon_url = db.Column(db.String(255), nullable=True)
    target_url = db.Column(db.String(255), nullable=False)
"""    
        

class Configs(db.Model):
    __tablename__="configs"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    theme = db.Column(db.String, nullable=False, default='light')
    view_mode = db.Column(db.String, nullable=False, default='grid')

    user = db.relationship('Users', back_populates='configs')
    
