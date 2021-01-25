"""Routes for API requests"""
from flask import request
from marshmallow import validate, ValidationError
from flask_restful import Resource, reqparse, abort

from photoric import db
from photoric.core.models import User, Role, Group, Album, Image, AlbumImage, check_object_name, check_object_exists
from photoric.modules.api import api_bp, mm, api
from photoric.modules.auth.helper import create_user, update_user


class UserSchema(mm.SQLAlchemySchema):
    class Meta:
        model = User
        load_instance = True

    id = mm.auto_field(dump_only=True)
    name = mm.auto_field(required=True, validate=validate.Length(min=3,
                                                                 error="Name must be at least 3 symbols long."))
    email = mm.Email(required=True)
    password = mm.auto_field(required=True,
                             validate=validate.Regexp('(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*(&|%|#)).{8,}',
                                             error='Password must contain at least one number, \
                                             one uppercase and lowercase letter, \
                                             one special symbol (&,$,#) and has at least \
                                             8 characters.')
                             )
    created_on = mm.auto_field(dump_only=True)
    active = mm.auto_field()
    last_login = mm.auto_field(dump_only=True)

    roles = mm.Nested(lambda: RoleSchema(many=True, exclude=("users", "_links")))
    groups = mm.Nested(lambda: GroupSchema(many=True, exclude=("users", "_links")))

    _links = mm.Hyperlinks(
        {
            "self": mm.URLFor("api.user_detail", values=dict(id="<id>")),
            # "roles": mm.URLFor("api.user_roles", values=dict(id="<id>")),
            # "groups": mm.URLFor("api.user_groups", values=dict(id="<id>")),
            "collection": mm.URLFor("api.users")
        }
    )
    

user_schema = UserSchema()
users_schema = UserSchema(many=True)


class UserApi(Resource):
    def get(self, id):
        # check if requested user exists
        user = check_object_exists(object_type='user', id=id)
        if not user:
            return {"message": "User was not found."}, 404
            
        # return serialized user details
        return {"user": user_schema.dump(user)}

    def put(self, id):
        # check if requested user exists
        user = check_object_exists(object_type='user', id=id)
        if not user:
            return {"message": "User was not found."}, 404

        # extract user data from request
        json_data = request.get_json()
        if not json_data:
            return {"message": "User data was not changes."}, 400
        
        # Validate and deserialize input
        try:
            data = user_schema.load(json_data, missing=None)
        except ValidationError as err:
            return err.messages, 422

        # update user
        user = user_schema.dump(update_user(data))
        return {"message": "User details were updated.", "user": user}, 200

    def delete(self, id):
        # check if requested user exists
        user = check_object_exists(object_type='user', id=id)
        if not user:
            return {"message": "User was not found."}, 404

        # delete user
        db.session.delete(user)
        db.session.commit()
        return {"message": "User was deleted."}, 204


class UsersApi(Resource):
    def get(self):
        users = User.query.all()
        return users_schema.dump(users)

    def post(self):
        # extract new user data from request
        json_data = request.get_json()
        if not json_data:
            return {"message": "New user data were not provided."}, 400
        
        # Validate input
        # errors = user_schema.validate(json_data)
        # if errors:
        #   return errors, 422
        # Validate and deserialize input
        try:
            data = user_schema.load(json_data)
        except ValidationError as err:
            return err.messages, 422

        # check if user with such name already exists
        if check_object_name(object_type="user", name=data.name):
            return {"message": "User with such name already exists."}, 400

        # create new user
        user = user_schema.dump(create_user(data))
        return {"message": "New user was created.", "user": user}, 201
            

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
