"""Routes for API requests"""
from flask import Blueprint
from flask_marshmallow import Marshmallow
from flask_restful import Api, Resource, reqparse, abort

from photoric.config.models import db, User, Album, Image, AlbumImage


# Blueprint initialization
photoric_api = Blueprint(
    'photoric_api', __name__,
    url_prefix='/api',
    template_folder='templates',
    static_folder='static',
    static_url_path='/static'
)


# Initialize serializer object
mm = Marshmallow()

# Initialize API object
api = Api()


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
