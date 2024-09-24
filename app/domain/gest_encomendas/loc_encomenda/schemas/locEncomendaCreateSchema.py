# locEncomendaCreateSchema.py


from marshmallow import Schema, fields, post_load

from ..locEncomenda import LocEncomenda


class LocEncomendaCreateSchema(Schema):

    # id = fields.Int()
    latitude = fields.Float(required=True)
    longitude = fields.Float(required=True)
    # id_encomenda = fields.Int(required=True)

    @post_load
    def make_loc_encomenda(self, data, **kwargs):
        """Desserializar dados para uma instância LocEncomenda"""
        return LocEncomenda(**data)
