from marshmallow import Schema, fields

from app.web.schemes import OkResponseSchema


class UserAddSchema(Schema):
    # при создании пользователя нам не нужен id
    email = fields.Str(required=True)  # графа email required-обязательная


class UserSchema(UserAddSchema): # модель пользователя предствляет собой email и id
    id = fields.UUID(required=True, attribute='id_')


class UserGetRequestSchema(Schema):
    id = fields.UUID(required=True)


class UserGetSchema(Schema):
    user = fields.Nested(UserSchema)


class UserGetResponseSchema(OkResponseSchema):
    data = fields.Nested(UserGetSchema)


class ListUsersSchema(Schema):
    users = fields.Nested(UserSchema, many=True)


class ListUsersResponseSchema(OkResponseSchema):
    data = fields.Nested(ListUsersSchema)
