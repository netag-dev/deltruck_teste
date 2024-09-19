# userLoginSchema.py

from marshmallow import Schema, fields, validate, post_load

from app.domain.gest_usuarios.user import User
from app.utils.validationUtils import ValidationUtils


class UserLoginSchema(Schema):
    user_email = fields.Str(
        required=True,
        validate=[ValidationUtils.email()],
    )
    password = fields.Str(
        required=True,
        validate=[ValidationUtils.password()],
    )
    auth_code = fields.Str(
        required=True,
    )

    @post_load
    def make_user(self, data, **kwargs):
        data.pop("auth_code", None)
        return User(**data)
