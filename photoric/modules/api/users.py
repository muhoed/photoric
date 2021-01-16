"""Routes for API requests"""
from flask import request
from flask_restful import Resource, reqparse, abort

from photoric.core.models import db, User, Role, Group, Album, Image, AlbumImage
from photoric.modules.api import api_bp, mm, api


class UserSchema(mm.SQLAlchemySchema):
    class Meta:
        model = User
        load_instance = True

    id = mm.auto_field(dump_only=True)
    name = mm.auto_field()
    email = mm.auto_field()
    created_on = mm.auto_field()
    active = mm.auto_field()
    last_login = mm.auto_field()

    roles = mm.Nested(lambda: RoleSchema(many=True, exclude=("users", "_links")))
    groups = mm.Nested(lambda: GroupSchema(many=True, exclude=("users", "_links")))

    _links = mm.Hyperlinks(
        {
            "self": mm.URLFor("api.user_detail", values=dict(id="<id>")),
            # "self.roles": mm.URLFor("user_roles", values=dict(id="<id>")),
            # "self.groups": mm.URLFor("user_groups", values=dict(id="<id>")),
            "collection": mm.URLFor("api.users")
        }
    ) 

user_schema = UserSchema()
users_schema = UserSchema(many=True)


class UserApi(Resource):
    def get(self, id):
        user = User.query.get_or_404(id)
        return user_schema.dump(user)

    def put(self, id):
        pass

    def delete(self, id):
        pass


class UsersApi(Resource):
    def get(self):
        users = User.query.all()
        return users_schema.dump(users)

    def post(self):
        json_data = request.get_json()
        pass

api.add_resource(UserApi, '/users/<int:id>', endpoint='user_detail')
api.add_resource(UsersApi, '/users', endpoint='users')


class RoleSchema(mm.SQLAlchemySchema):
    class Meta:
        model = Role
        load_instance = True

    id = mm.auto_field()
    name = mm.auto_field()
    restrictions = mm.auto_field()

    users = mm.Nested(UserSchema, many=True, exclude=("roles", "_links"))

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

    users = mm.Nested(UserSchema, many=True, exclude=("groups", "_links"))

    _links = mm.Hyperlinks(
        {
            "self": mm.URLFor("group_detail", values=dict(id="<id>")),
            "self.users": mm.URLFor("group_users", values=dict(id="<id>")),
            "collection": mm.URLFor("groups")
        }
    )

group_schema = RoleSchema()
groups_schema = RoleSchema(many=True)
