# EncomendaEditSchema.py

from marshmallow import Schema, fields, post_load
from app.domain.gest_pessoas.pessoa.schemas import PessoaEditSchema
from app.domain.gest_encomendas.transportadora.shemas import TransportadoraEditSchema

from ..encomenda import Encomenda


class EncomendaEditSchema(Schema):
    """Esse schema pode ser usado tanto para:

    1. Response: Os dados retornados na resposta são utilizados em requisições PUT
    2. Request: Para validar e carregar os dados do cliente em requisições PUT
    """

    id = fields.Int()
    # data_encomenda = fields.DateTime(format="%Y-%m-%d %H:%M:%S")
    id_pessoa_cliente_final = fields.Int()
    id_transportadora = fields.Int()
    id_status_encomenda = fields.Int()

    pessoa_cliente_final = fields.Nested(
        PessoaEditSchema, only=("id", "primeiro_nome", "ultimo_nome")
    )
    transportadora = fields.Nested(TransportadoraEditSchema, only=("id", "nome"))
    id_status_encomenda = fields.Int()

    @post_load
    def make_encomenda(self, data, **kwargs):
        return Encomenda(**data)
