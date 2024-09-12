# enderecoEditSchema.py

from marshmallow import Schema, fields, post_load

from app.domain.gest_pessoas.cidade.schemas import CidadeEditSchema

from ..endereco import Endereco


class EnderecoEditSchema(Schema):

    id = fields.Int()
    linha_1 = fields.Str(missing=None)
    linha_2 = fields.Str(missing=None)
    bairro = fields.Str(missing=None)
    cidade = fields.Nested(CidadeEditSchema)

    @post_load
    def make_user(self, data, **kwargs):
        return Endereco(**data)
