from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_login import UserMixin
from flask_authorize import RestrictionMixin, AllowancesMixin
from flask_authorize import PermissionMixin
from werkzeug.security import generate_password_hash, check_password_hash


db = SQLAlchemy()

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
    db.Column('id',
              db.Integer,
              db.ForeignKey('albums.id'))
    db.Column('id',
              db.Integer,
              db.ForeignKey('images.id'))
)    

# declare models    

# base class for gallery items
class GalleryItems(db.Model):
    __tablename__='gallery_item'
    
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(50))
    name = db.Column(db.String(100), unique=True, nullable=True)
    description = db.Column(db.String(500), nullable=True)
    keywords = db.Column(db.String(255), nullable=True)
    created_on = db.Column(db.DateTime, nullable=False, default=datetime.now)
    publicated = db.Column(db.Boolean(), nullable=False, default=False)

    __mapper_args__ = {
        'polymorphic_identity':'gallery_item',
        'polymorphic_on':type
    }
    

class Images(GalleryItems):
    __tablename__="images"
    __permissions__ = dict(
        owner=['read', 'update', 'delete', 'revoke'],
        group=['read', 'update'],
        other=['read']
    )
    id = db.Column(db.Integer, db.ForeignKey('gallery_item.id'), primary_key=True)
    filename = db.Column(db.String, unique=True, nullable=False)
    uploaded_on = db.Column(db.DateTime, nullable=False, default=datetime.now)
    location = db.Column(db.String, nullable=True)
    parent = db.relationship(
        'Albums',
        secondary=albums_images,
        back_populates='children_images')

    __mapper_args__ = {
        'polymorphic_identity:'images',
    }
    
    def __repr__(.self):
        return '<Image %r>' % self.filename
    

class Albums(GalleryItems):
    __tablename__="albums"
    __permissions__ = dict(
        owner=['read', 'update', 'delete', 'revoke'],
        group=['read', 'update'],
        other=['read']
    )
    id = db.Column(db.Integer, primary_key=True)
    parent_id = db.Column(db.Integer, db.ForeignKey('albums.id')
    icon = db.Column(db.String, nullable=False)                                      
    children_images = db.relationship(
        'Images',
        secondary=albums_images,
        back_populates='parent')
    children_albums = db.relationship(
        'Albums', backref=backref('parent', remote_side=[id])
    
    __mapper_args__ = {
        'polymorphic_identity:'albums',
    }

    def __repr__(.self):
        return '<Album %r>' % self.name
        

class Users(UserMixin, db.Model):
    __tablename__="users"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True, nullable=False)
    access = db.Column(db.String, nullable=False, default='guest')
    email = db.Column(db.String, nullable=False)
    password_hash = db.Column(db.String, nullable=False)
    created_on = db.Column(db.DateTime, nullable=False, default=datetime.now)
    lasl_login = db.Column(db.DateTime, nullable=True)                                      

    def hash_email(.self, password):
        """create hashed password"""
        self.password_hash = generate_password_hash(password, method='sha256')

    def check_password(.self, password):
        """check hashed password"""
        return check_password_hash(self.password, password)
    
    def __repr__(.self):
        return '<User %>' % self.name
        

class Groups(db.Model, RestrictionsMixin):
    __tablename__='groups'                             
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
        

class Roles(db.Model, RestrictionsMixin):
    __tablename__='roles'                             
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
        

class Configs(db.Model):
    __tablename__="configs"
    id = db.Column(db.Integer, primary_key=True)
    id = db.Column(db.Integer, ForeignKey('users.id'), nullable=False)
    theme = db.Column(db.String, nullable=False, default='light')
    view_mode = db.Column(db.String, nullable=False, default='grid')

    user = db.relationship('Users', back_populates='configs')
    
