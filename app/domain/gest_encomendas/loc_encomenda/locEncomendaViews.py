# locEncomendaApi.py

import logging

from flask import request, jsonify, json
from flask.views import MethodView

from app.utils.schemaUtils import SchemaUtils
from app.utils.hateoasLinkGenerator import HateoasLinkGenerator

from .locEncomendaService import LocEncomendaService
from .schemas import LocEncomendaCreateSchema, LocEncomendaResponseSchema


class LocEncomendaApi(MethodView):
    def __init__(self):
        super().__init__()
        self.loc_encomenda_service = LocEncomendaService()
        self.hateos_link_generator = HateoasLinkGenerator(
            {
                "self": "loc_encomenda_api",
            },
            resource_id="loc_encomenda_id",
        )

    def post(self, encomenda_id):

        logging.info("0: LocEncomendaApi.post")

        loc_encomenda_data = request.get_json()

        loc_encomenda = SchemaUtils.deserialize(
            LocEncomendaCreateSchema(), loc_encomenda_data
        )

        loc_encomenda.id_encomenda = encomenda_id
        logging.info("1: LocEncomendaApi.post")

        loc_encomenda_update = self.loc_encomenda_service.update_encomenda_location(
            loc_encomenda
        )

        logging.info("2: LocEncomendaApi.post")

        # retorna uma resposta com status 201 (CREATED) e corpo contendo os dados da loc_encomenda.
        return (
            jsonify(
                SchemaUtils.serialize(
                    LocEncomendaResponseSchema(), loc_encomenda_update
                )
            ),
            201,
        )
