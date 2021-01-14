"""Routes for API requests"""
from flask_restful import Resource, reqparse, abort

from photoric.core.models import db, User, Role, Group, Album, Image, AlbumImage
from photoric.modules.api import api_bp, mm, api


class UserSchema(mm.SQLAlchemySchema):
    class Meta:
        model = User
        load_instance = True

    id = mm.auto_field()
    name = mm.auto_field()
    email = mm.auto_field()
    created_on = mm.auto_field()
    active = mm.auto_field()
    last_login = mm.auto_field()

    roles = mm.auto_field()  # mm.Nested(RoleSchema(), many=True, exclude=("users", "_links"))
    groups = mm.auto_field()  # mm.Nested(GroupSchema(), many=True, exclude=("users", "_links"))

    _links = mm.Hyperlinks(
        {
            "self": mm.URLFor("user_detail", values=dict(id="<id>")),
            "self.roles": mm.URLFor("user_roles", values=dict(id="<id>")),
            "self.groups": mm.URLFor("user_groups", values=dict(id="<id>")),
            "collection": mm.URLFor("users")
        }
    )

user_schema = UserSchema()
users_schema = UserSchema(many=True)

class RoleSchema(mm.SQLAlchemySchema):
    class Meta:
        model = Role
        load_instance = True

    id = mm.auto_field()
    name = mm.auto_field()
    restrictions = mm.auto_field()

    users = mm.Nested(UserSchema(), many=True, exclude=("roles", "_links"))

    _links = mm.Hyperlinks(
        {
            "self": mm.URLFor("role_detail", values=dict(id="<id>")),
            "self.users": mm.URLFor("role_users", values=dict(id="<id>")),
            "collection": mm.URLFor("roles")
        }
    )

role_schema = RoleSchema()
roles_schema = RoleSchema(many=True)

class GroupSchema(mm.SQLAlchemySchema):
    class Meta:
        model = Group
        load_instance = True

    id = mm.auto_field()
    name = mm.auto_field()
    allowances = mm.auto_field()

    users = mm.Nested(UserSchema(), many=True, exclude=("groups", "_links"))

    _links = mm.Hyperlinks(
        {
            "self": mm.URLFor("group_detail", values=dict(id="<id>")),
            "self.users": mm.URLFor("group_users", values=dict(id="<id>")),
            "collection": mm.URLFor("groups")
        }
    )

role_schema = RoleSchema()
roles_schema = RoleSchema(many=True)


class UserApi(Resource):
    def get(self, id):
        pass

    def put(self, id):
        pass

    def post(self):
        pass

    def delete(self, id):
        pass
