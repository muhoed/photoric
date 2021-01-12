"""Routes for API requests"""
from flask_restful import Resource, reqparse, abort

from photoric.core.models import db, User, Album, Image, AlbumImage
from photoric.modules.api import api_bp


class UserSchema(mm.SQLAlchemySchema):
    class Meta:
        model = User

    id = mm.auto_field()
    name = mm.auto_field()
    email = mm.auto_field()
    created_on = mm.auto_field()
    active = mm.auto_field()
    last_login = mm.auto_field()

    roles = mm.auto_field()
    groups = mm.auto_field()


class UserApi(Resource):
    def get(self, id):
        pass

    def put(self, id):
        pass

    def post(self):
        pass

    def delete(self, id):
        pass
