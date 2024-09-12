# statusEncomendaResponseSchema.py


from marshmallow import Schema, fields


class StatusEncomendaResponseSchema(Schema):
    id = fields.Int()
    nome = fields.Str()
