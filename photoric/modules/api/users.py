from flask import request
from flask_restful import Resource
from marshmallow import ValidationError

from photoric.modules.api import api
from photoric.modules.auth.models import User, Role, Group
from photoric.modules.auth.schemas import UserSchema, RoleSchema, GroupSchema


class UserApi(Resource):
    def get(self, id):
        # check if requested user exists
        user = User.get_by_id(id=id)
        if not user:
            return {"message": "User was not found."}, 404
            
        # return serialized user details
        return {"user": UserSchema().dump(user)}

    def put(self, id):
        
        # extract user data from request
        json_data = request.get_json()
        if not json_data:
            return {"message": "User was not changes."}, 400
        
        # Validate and deserialize input
        try:
            data = UserSchema().load(json_data, partial=True)
        except ValidationError as err:
            return err.messages, 422

        # update user
        update_result = User.update_from_json(data, id)
        if isinstance(update_result, User):
            return {"message": "User details were updated.", "user": UserSchema().dump(update_result)}, 200
		
        return update_result

    def delete(self, id):
        if not User.delete(id):
            return {"message": "User was not found."}, 404

        return {"message": "User was deleted."}, 204


class UsersApi(Resource):
    def get(self):
        users = User.query.all()
        return UserSchema(many=True).dump(users)

    def post(self):
        # extract new user data from request
        json_data = request.get_json()
        if not json_data:
            return {"message": "New user details were not provided."}, 400
            
        # Validate and deserialize input
        try:
            data = UserSchema().load(json_data)
        except ValidationError as err:
            return err.messages, 422
        
        # create new user
        result = User.create_from_json(json_data)
        if isinstance(result, User):
            return {"message": "New user was created.", "user": UserSchema().dump(result)}, 201
        
        return result

api.add_resource(UserApi, '/users/<int:id>', endpoint='user_detail')
api.add_resource(UsersApi, '/users', endpoint='users')


class RoleApi(Resource):
    def get(self, id):
        # check if requested user exists
        role = Role.get_by_id(id=id)
        if not role:
            return {"message": "Role was not found."}, 404
            
        # return serialized role details
        return {"role": RoleSchema().dump(role)}

    def put(self, id):
        # check if requested role exists
        pass

    def delete(self, id):
        if not Role.delete(id):
            return {"message": "Role was not found."}, 404

        return {"message": "Role was deleted."}, 204


class RolesApi(Resource):
    def get(self):
        roles = Role.query.all()
        return RoleSchema(many=True).dump(roles)

    def post(self):
        # extract new role data from request
        json_data = request.get_json()
        if not json_data:
            return {"message": "New role data were not provided."}, 400
        
        # Validate and deserialize input
        try:
            data = RoleSchema().load(json_data)
        except ValidationError as err:
            return err.messages, 422

        # check if role with such name already exists
        if Role.get_by_name(name=data.name):
            return {"message": "Role with such name already exists."}, 400

        # create new role
        #role = role_schema.dump(create_role(data))
        #return {"message": "New role was created.", "role": role}, 201
        pass    

api.add_resource(RoleApi, '/roles/<int:id>', endpoint='role_detail')
api.add_resource(RolesApi, '/roles', endpoint='roles')
