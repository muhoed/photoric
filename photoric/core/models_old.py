from sqlalchemy.orm import backref
from sqlalchemy.ext.hybrid import hybrid_property
from datetime import datetime
from flask_login import UserMixin
from flask_authorize import RestrictionsMixin, AllowancesMixin, PermissionsMixin
from werkzeug.security import generate_password_hash, check_password_hash

from photoric import db
from photoric.modules.api.users import user_schema


# db = SQLAlchemy()
# migrate = Migrate()

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


AlbumImage = db.Table('album_image',
                      db.Column('album_id',
                                db.Integer,
                                db.ForeignKey('albums.id')),
                      db.Column('image_id',
                                db.Integer,
                                db.ForeignKey('images.id'))
)    

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
    # parent_id=db.Column(db.Integer, db.ForeignKey('albums.id'))
    description = db.Column(db.String(500), nullable=True)
    keywords = db.Column(db.String(255), nullable=True)
    filename = db.Column(db.String, unique=True, nullable=False)
    url = db.Column(db.String(255), nullable=False)
    uploaded_on = db.Column(db.DateTime, nullable=False, default=datetime.now)
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
    _password = db.Column("password", db.String, nullable=False)
    _created_on = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    _is_active = db.Column(db.Boolean, nullable=False, default=True)
    _last_login = db.Column(db.DateTime, nullable=True)

    _roles = db.relationship('Role', secondary=UserRole)
    _groups = db.relationship('Group', secondary=UserGroup)

    @property
    def is_authenticated(self):
        return True

    @property
    def is_anonymous(self):
        return False

    @hybrid_property
    def created_on(self):
        return self._created_on.strftime("%c")

    @hybrid_property
    def is_active(self):
        return self._is_active

    @is_active.setter
    def is_active(self, status=True):
        self._is_active = status

    @hybrid_property
    def password(self):
        return self._password

    @password.setter
    def password(self, password):
        self._password = generate_password_hash(password, method='sha256')

    #def new_password(self, password):
    #    self.password = self.hash_password(password)

    #def hash_password(self, password):
    #    """create hashed password"""
    #    return generate_password_hash(password, method='sha256')
    
    # check hashed password
    def check_password(self, password):
        return check_password_hash(self._password, password)

    @hybrid_property
    def last_login(self):
        return _last_login.strftime("%c")

    def set_last_login(self):
        self._last_login = datetime.utcnow()
        db.session.commit()

    def get_id(self):
        return self.id

    #def __init__(self, password=None, password_hash=None, **kwargs):
    #    if password_hash is None and password is not None:
    #        password_hash = self.hash_password(password)
    #    super().__init__(password=password_hash, **kwargs)

    @hybrid_property
    def roles(self):
        return self._roles

    @roles.setter
    def roles(self, roles):
        for role in roles:
            existing_role = check_object_name(object_type='role', name=role.name)
            if existing_role:
                self._roles.append(existing_role)
            else:
                self._roles = self._roles.append(roles)

    @hybrid_property
    def groups(self):
        return self._groups

    @groups.setter
    def groups(self, groups):
        for group in groups:
            existing_group = check_object_name(object_type='group', name=group.name)
            if existing_group:
                self._groups.append(existing_group)
            else:
                self._groups = self._groups.append(group)

    @classmethod
    def from_json(cls, json_data):

        # check if user with such name already exists
        if "name" in json_data and cls.get_by_name(json_data["name"]):
            return {"message": "User with such name already exists."}, 400
        
        # Validate and deserialize input
        try:
            data = user_schema.load(json_data)
        except ValidationError as err:
            return err.messages, 422

        # set roles and groups using db instances if any
        if data.roles:
            data.roles(data.roles)
        if data.groups:
            data.groups(data.groups)

        db.session.add(new_user)
        db.session.commit

        return cls.get_by_name(new_user.name)

    @classmethod
    def get_by_id(cls, id):
        if not id:
            return False
        try:
            instance = cls.query.get(id)
        except IntegrityError:
            return False
        return instance

    @classmethod
    def get_by_name(cls, name):
        if not name:
            return False
        instance = cls.query.filter_by(name=name).first()
        if instance:
            return instance
        return False

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

    classmethod
    def get_by_id(cls, id):
        if not id:
            return False
        try:
            instance = cls.query.get(id)
        except IntegrityError:
            return False
        return instance

    @classmethod
    def get_by_name(cls, name):
        if not name:
            return False
        instance = cls.query.filter_by(name=name).first()
        if instance:
            return instance
        return False
        

class Role(db.Model, RestrictionsMixin):
    __tablename__='roles'

    __restrictions__ = {}

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)

    classmethod
    def get_by_id(cls, id):
        if not id:
            return False
        try:
            instance = cls.query.get(id)
        except IntegrityError:
            return False
        return instance

    @classmethod
    def get_by_name(cls, name):
        if not name:
            return False
        instance = cls.query.filter_by(name=name).first()
        if instance:
            return instance
        return False
    

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
        return requested_object
    return False

def check_object_exists(object_type=None, id=None):
    if object_type is None or id is None:
        return False
    try:
        requested_object = db.session.query(models[object_type]).get(id)
    except IntegrityError:
            return False

    return requested_object
