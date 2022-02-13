from sqlalchemy.orm import backref
from sqlalchemy.ext.hybrid import hybrid_property
from datetime import datetime
from flask_login import UserMixin
from flask_authorize import RestrictionsMixin, AllowancesMixin, PermissionsMixin
from werkzeug.security import generate_password_hash, check_password_hash

from photoric import db
from photoric.core.mixins import PhotoricMixin
from photoric.modules.auth import login_manager


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


class User(PhotoricMixin, UserMixin, db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False, unique=True)
    email = db.Column(db.String, )
    _password = db.Column(db.String, nullable=False)
    _created_on = db.Column(db.DateTime, nullable=False, default=datetime.utcnow())
    _is_active = db.Column(db.Boolean, nullable=False, default=True)
    _last_login = db.Column(db.DateTime, nullable=True)

    _roles = db.relationship('Role', secondary=UserRole)
    _groups = db.relationship('Group', secondary=UserGroup)

    @hybrid_property
    def created_on(self):
        return self._created_on  # .strftime("%c")

    @hybrid_property
    def is_active(self):
        return self._is_active

    @is_active.setter
    def is_active(self, status=True):
        self._is_active = status

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, password):
        self._password = generate_password_hash(password, method='sha256')

    def check_password(self, password):
        return check_password_hash(self._password, password)

    @hybrid_property
    def last_login(self):
        return self._last_login  # .strftime("%c")

    @last_login.setter
    def last_login(self, trigger):
        if trigger == "set":
            self._last_login = datetime.utcnow()
            db.session.commit()
        else:
            pass

    @hybrid_property
    def roles(self):
        return self._roles

    @roles.setter
    def roles(self, roles):
        missed = self._build_relationship("_roles", roles, Role, True)
        if missed != []:
            msg = "The following roles do not exist and were not added: {}.".format(missed)
            return {"message":msg}, 404

    @hybrid_property
    def groups(self):
        return self._groups

    @groups.setter
    def groups(self, groups):
        missed = self._build_relationship("_groups", groups, Group, True)
        if missed != []:
            msg = "The following groups do not exist and were not added: {}.".format(missed)
            return {"message":msg}, 404
    
    # Required for administrative interface
    def __unicode__(self):
        return self.name
    
    def __repr__(self):
        return '<User %r>' % self.name


#callback for Flask-Login
@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))


class Group(db.Model, AllowancesMixin, PhotoricMixin):
    __tablename__ = 'groups'

    __allowances__ = {}

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    
    _users = db.relationship('User', secondary=UserGroup)
    
    @hybrid_property
    def users(self):
        return self._users

    @users.setter
    def users(self, users):
        for user in users:
            existing_user = User.get_by_name(name=user["name"])
            if existing_user:
                self._users.append(existing_user)
            else:
                return {"message":"User does not exist. Only existing user(-s) can be included in a group"}, 404
                
    def __repr__(self):
        return '<Group %r>' % self.name
        

class Role(db.Model, RestrictionsMixin, PhotoricMixin):
    __tablename__='roles'

    __restrictions__ = {}

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    
    _users = db.relationship('User', secondary=UserRole)
    
    @hybrid_property
    def users(self):
        return self._users

    @users.setter
    def users(self, users):
        for user in users:
            existing_user = User.get_by_name(name=user["name"])
            if existing_user:
                self._users.append(existing_user)
            else:
                return {"message":"User is not exists. Role can be assigned to existing user(-s) only"}, 404
                
    def __repr__(self):
        return '<Role %r>' % self.name
