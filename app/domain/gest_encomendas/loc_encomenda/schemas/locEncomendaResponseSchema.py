# locEncomendaResponseSchema.py


from marshmallow import Schema, fields

from app.domain.gest_encomendas.encomenda.schemas import EncomendaResponseSchema


class LocEncomendaResponseSchema(Schema):
    id = fields.Int()
    latitude = fields.Float(required=True)
    longitude = fields.Float(required=True)
    id_encomenda = fields.Int(required=True)
    # encomenda = fields.Nested(EncomendaResponseSchema)
