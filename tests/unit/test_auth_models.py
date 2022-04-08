import datetime
import pytest

from photoric import db
from photoric.modules.auth.models import User, Group, Role


@pytest.fixture
def user(app):

    user = User(
        name = "Test user",
        email = 'test@test.com',
        password = 'test_password'
        )
    db.session.add(user)
    db.session.commit()
    
    yield user

    db.session.delete(user)
    db.session.commit()

@pytest.fixture
def group(app):

    group = Group(
        name = "test_group",
        allowances = "*"
        )
    db.session.add(group)
    db.session.commit()
    
    yield group

    db.session.delete(group)
    db.session.commit()

@pytest.fixture
def rolw(app):

    role = Role(
        name = "test_role",
        restrictions = {}
        )
    db.session.add(role)
    db.session.commit()
    
    yield group

    db.session.delete(role)
    db.session.commit()

def test_new_user(user):
    """
    GIVEN an User model
    WHEN a new User is created
    THEN check 'created_on' is equal to current date, 'password' is hashed,
    'check_password' works as expected, '__repr__' method returns user name
    """
    assert user.created_on.date() == datetime.datetime.utcnow().date()
    assert user.password != 'test_password'
    assert user.check_password('test_password') is True
    assert user.is_active is True

    assert str(user) == "<User 'Test user'>"

def test_user_properties(user):
    """
    GIVEN an User model
    WHEN a new User is created
    THEN 'is_active' is True and respective setter works as expected, 
    'last_login', 'roles', 'group' getter/setter work as expected
    """

    # is_active
    assert user.is_active is True
    user.is_active = False
    assert user.is_active is False

    # last_login
    assert user.last_login is None
    user.last_login = 'set'
    assert user.last_login.date() == datetime.datetime.utcnow().date()

    # roles
    assert user.roles == []
    # non-existing role
    user.roles = [{'name':'new_role', 'restrictions':{}},]
    db.session.commit()
    assert Role.query.filter_by(name='new_role').first() in user.roles
    
    # groups
    assert user.groups == []
    # non-existing role
    user.groups = [{'name':'new_group', 'allowances':'*'},]
    db.session.commit()
    assert Group.query.filter_by(name='new_group').first() in user.groups


