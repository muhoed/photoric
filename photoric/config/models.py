from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash


ph_db = SQLAlchemy()

# map tables to classes
album_items = ph_db.Table('album_items',
    ph.db.Column('album_id', ph_db.Integer, db.ForeignKey('albums.album_id'), primary_key=True)
    ph_db.Column('image_id', ph_db.Integer, db.ForeignKey('images.image_id'), primary_key=True)
)    

class Images(ph_db.Model):
    __tablename__="images"
    image_id = ph_db.Column(ph_db.Integer, primary_key=True)
    image_filename = ph_db.Column(ph_db.String, unique=True, nullable=False)
    image_name = ph_db.Column(ph_db.String(80), unique=True, nullable=True)
    image_description = ph_db.Column(ph_db.Text, nullable=True)
    image_keywords = ph_db.Column(ph_db.Text, nullable=True)
    image_created_on = ph_db.Column(ph_db.DateTime, nullable=False, default=datetime.now)
    image_uploaded_on = ph_db.Column(ph_db.DateTime, nullable=False, default=datetime.now)
    image_location = ph_db.Column(ph_db.String, nullable=True)
    image_access = ph_db.Column(ph_db.String(10), nullable=False, default='auth')
    image_albums = ph_db.relationship('Albums', secondary=album_items, back_populates='images')

    def __repr__(.self):
        return '<Image %r>' % self.filename

category_items = ph_db.Table('category_items',
    ph.db.Column('album_id', ph_db.Integer, db.ForeignKey('albums.album_id'), primary_key=True)
    ph_db.Column('category_id', ph_db.Integer, db.ForeignKey('categories.category_id'), primary_key=True)
) 

class Albums(ph_db.Model):
    __tablename__="albums"
    album_id = ph_db.Column(ph_db.Integer, primary_key=True)
    album_parent_album = ph_db.Column(ph_db.Integer, ph_db.ForeignKey('albums.album_id')
    album_name = ph_db.Column(ph_db.String(80), unique=True,  nullable=True)
    album_description = ph_db.Column(ph_db.Text, nullable=True)
    album_keywords = ph_db.Column(ph_db.Text, nullable=True)
    album_created_on = ph_db.Column(ph_db.DateTime, nullable=False, default=datetime.now)
    album_icon = ph_db.Column(ph_db.String, nullable=False)
    album_access = ph_db.Column(ph_db.String(10), nullable=False, default='auth')                                      
    album_images = ph_db.relationship('Images', secondary=album_items, back_populates='albums')
    album_categories = ph_db.relationship('Categories', secondary=category_items, back_populates='albums')
    album_parent = ph_db.relationship('Albums', back_populates='albums')

    def __repr__(.self):
        return '<Album %r>' % self.album_name   

class Categories(ph_db.Model):
    __tablename__="categories"
    category_id = ph_db.Column(ph_db.Integer, primary_key=True)
    category_name = ph_db.Column(ph_db.String(80), unique=True, nullable=True)
    category_description = ph_db.Column(ph_db.Text, nullable=True)
    category_keywords = ph_db.Column(ph_db.Text, nullable=True)
    category_created_on = ph_db.Column(ph_db.DateTime, nullable=False, default=datetime.now)
    category_access = ph_db.Column(ph_db.String(10), nullable=False, default='auth')                                      
    category_icon = ph_db.Column(ph_db.String, nullable=False)
    category_albums = ph_db.relationship('Albums', secondary=category_items, back_populates='categories')

    def __repr__(.self):
        return '<Category %r>' % self.category_name

class Users(UserMixin, ph_db.Model):
    __tablename__="users"
    user_id = ph_db.Column(ph_db.Integer, primary_key=True)
    user_name = ph_db.Column(ph_db.String, unique=True, nullable=False)
    user_access = ph_db.Column(ph_db.String, nullable=False, default='guest')
    user_email = ph_db.Column(ph_db.String, nullable=False)
    user_password_hash = ph_db.Column(ph_db.String, nullable=False)
    user_created_on = ph_db.Column(ph_db.DateTime, nullable=False, default=datetime.now)
    user_lasl_login = ph_db.Column(ph_db.DateTime, nullable=True)                                      

    def hash_email(.self, password):
        """create hashed password"""
        self.user_password_hash = generate_password_hash(password, method='sha256')

    def check_password(.self, password):
        """check hashed password"""
        return check_password_hash(self.password, password)
    
    def __repr__(.self):
        return '<User %>' % self.user_name

class Configs(ph_db.Model):
    __tablename__="configs"
    config_id = ph_db.Column(ph_db.Integer, primary_key=True)
    config_user_id = ph_db.Column(ph_db.Integer, ForeignKey('users.user_id'), nullable=False)
    config_theme = ph_db.Column(ph_db.String, nullable=False, default='light')
    config_view_mode = ph_db.Column(ph_db.String, nullable=False, default='grid')

    user = ph_db.relationship('Users', back_populates='configs')
    
