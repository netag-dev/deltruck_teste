# encomendaResponseSchema.py


from marshmallow import Schema, fields
from app.domain.gest_pessoas.pessoa.schemas import (
    PessoaResponseSchema,
)  # Importe o schema PessoaResponseSchema se necessário
from app.domain.gest_encomendas.transportadora import TransportadoraResponseSchema
from app.domain.gest_encomendas.status_encomenda.schemas import (
    StatusEncomendaResponseSchema,
)


class EncomendaResponseSchema(Schema):
    id = fields.Int()
    data_encomenda = fields.DateTime()
    id_pessoa_cliente_final = fields.Int()
    id_transportadora = fields.Int()
    status_encomenda = fields.Nested(StatusEncomendaResponseSchema, only=("nome",))

    # Opcional
    pessoa_cliente_final = fields.Nested(PessoaResponseSchema, only=("primeiro_nome",))
    transportadora = fields.Nested(TransportadoraResponseSchema, only=("nome",))
