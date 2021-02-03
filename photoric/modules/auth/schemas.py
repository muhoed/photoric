from marshmallow import validate

from photoric import mm
from .models import User, Role, Group


# (de)serialization schemas for User, Role and Group classes
class UserSchema(mm.SQLAlchemySchema):
    class Meta:
        model = User
        # load_instance = True

    id = mm.auto_field(dump_only=True)
    name = mm.auto_field(required=True, validate=validate.Length(min=3,
                                                                 error="Name must be at least 3 symbols long."))
    email = mm.Email(required=True)
    password = mm.String(load_only=True, required=True,
                             validate=validate.Regexp('(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*(&|$|#)).{8,}',
                                             error='Password must contain at least one number, \
                                             one uppercase and lowercase letter, \
                                             one special symbol (&,$,#) and has at least \
                                             8 characters.')
                             )
    created_on = mm.DateTime(dump_only=True)
    is_active = mm.Boolean()
    last_login = mm.DateTime(dump_only=True)

    roles = mm.Nested(lambda: RoleSchema(many=True, exclude=("users", "_users_links", "_links")))
    groups = mm.Nested(lambda: GroupSchema(many=True, exclude=("users", "_users_links", "_links")))

    _roles_links = mm.List(mm.HyperlinkRelated("api.role_detail", attribute="roles"), attribute="roles", dump_only=True)
    # _groups_links = mm.List(mm.HyperlinkRelated("api.group_detail", attribute="groups"), attribute="groups", dump_only=True)
    
    _links = mm.Hyperlinks(
        {
            "self": mm.URLFor("api.user_detail", values=dict(id="<id>")),
            "collection": mm.URLFor("api.users")
        }
    )


class RoleSchema(mm.SQLAlchemySchema):
    class Meta:
        model = Role
        # load_instance = True

    id = mm.auto_field(dump_only=True)
    name = mm.auto_field(validate=validate.Length(min=1, error="Name must be at least 1 symbols long."))
    restrictions = mm.auto_field()

    users = mm.Nested(lambda: UserSchema(many=True, only=("id", "name")))
    
    _users_links = mm.List(mm.HyperlinkRelated("api.user_detail", attribute="users"), attribute="users", dump_only=True)

    _links = mm.Hyperlinks(
        {
            "self": mm.URLFor("api.role_detail", values=dict(id="<id>")),
            "collection": mm.URLFor("api.roles")
        }
    )


class GroupSchema(mm.SQLAlchemySchema):
    class Meta:
        model = Group
        # load_instance = True

    id = mm.auto_field(dump_only=True)
    name = mm.auto_field(validate=validate.Length(min=1, error="Name must be at least 1 symbols long."))
    allowances = mm.auto_field()

    users = mm.Nested(lambda: UserSchema(many=True, only=("id", "name")))
    
    _users_links = mm.List(mm.HyperlinkRelated("api.user_detail", attribute="users"), attribute="users", dump_only=True)

    _links = mm.Hyperlinks(
        {
            "self": mm.URLFor("api.group_detail", values=dict(id="<id>")),
            "collection": mm.URLFor("api.groups")
        }
    )
