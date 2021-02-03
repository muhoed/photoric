from sqlalchemy.orm import backref
from datetime import datetime
from flask_authorize import RestrictionsMixin, AllowancesMixin, PermissionsMixin

from photoric import db


# Photoric base model class provides common properties
# and methods
class PhotoricMixin():

    @classmethod
    def get_by_id(cls, id=None):
        if id is None:
            return False
        try:
            instance = cls.query.get(id)
        except IntegrityError:
            return False
        return instance

    @classmethod
    def get_by_name(cls, name=None):
        if name is None:
            return False
        instance = cls.query.filter_by(name=name).first()
        if instance:
            return instance
        return False

    @classmethod
    def create_from_json(cls, data):

        # check if object with such name already exists
        if cls.get_by_name(name=data["name"]):
            msg = "%s with such name already exists." % cls.__name__
            return {"message": msg}, 400
            
        obj = cls()
        for key, value in data.items():
            setattr(obj, key, value)

        db.session.add(obj)
        db.session.commit()

        return cls.get_by_name(obj.name)

    @classmethod
    def update_from_json(cls, data, id):
		
		# check if requested object exists
        obj = cls.get_by_id(id=id)
        if not object:
            msg = "%s was not found" % cls.__name__
            return {"message": msg}, 404
            
        if "name" in data and data["name"] != obj.name and cls.get_by_name(name=data["name"]):
            return {"message": "This name is already in use. Please use a different name."}, 400
        
        for key, value in data.items():
            setattr(obj, key, value)	
        db.session.commit()
		
        return obj

    @classmethod
    def delete(cls, id=None):
        if id is None:
            return False
        instance = cls.query.get(id)
        if not instance:
            return False
        db.session.delete(instance)
        db.session.commit()
        return True
        
    def _build_relationship(self, rel, data, rel_cls, create=False):
        missed = []
        for item in data:
            existing_item = rel_cls.get_by_name(name=item["name"])
            if existing_item:
                getattr(self, rel).append(existing_item)
            elif create:
                new_item = rel_cls.create_from_json(item)
                getattr(self, rel).append(new_item)
            else:
                missed.append(item["name"])
        return missed


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
