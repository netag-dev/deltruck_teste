# encomendaViews.py

import logging

from flask import request, jsonify, json
from flask.views import MethodView

from app.utils.schemaUtils import SchemaUtils
from app.utils.hateoasLinkGenerator import HateoasLinkGenerator

from app.domain.gest_encomendas.encomenda import EncomendaService
from app.domain.gest_encomendas.encomenda.schemas import (
    EncomendaCreateSchema,
    EncomendaResponseSchema,
    EncomendaEditSchema,
)


class EncomendaApi(MethodView):
    def __init__(self):
        super().__init__()
        self.encomenda_service = EncomendaService()
        self.hateos_link_generator = HateoasLinkGenerator(
            {
                "self": "encomenda_api",
            },
            resource_id="encomenda_id",
        )

    def post(self):
        encomenda_data = request.get_json()

        encomenda = SchemaUtils.deserialize(EncomendaCreateSchema(), encomenda_data)

        logging.debug("0: EncomendaApi.post")

        encomenda_criado = self.encomenda_service.create(encomenda)

        logging.info("1: EncomendaApi.post")

        # retorna uma resposta com status 201 (CREATED) e corpo contendo os dados da encomenda.
        return (
            jsonify(SchemaUtils.serialize(EncomendaResponseSchema(), encomenda_criado)),
            201,
        )

    def get(self, encomenda_id=None):
        if encomenda_id is None:
            return self._get_all()
        else:
            return self._get_encomenda(encomenda_id)

    def _get_all(self):
        """ """
        encomendas = self.encomenda_service.get_all()
        # Retorna uma resposta com status 200 (OK) e corpo contendo a lista de encomendas
        return (
            jsonify(SchemaUtils.serialize(EncomendaResponseSchema(), encomendas)),
            200,
        )

    def _get_encomenda(self, encomenda_id):
        """ """
        encomenda = self.encomenda_service.get_by_id(encomenda_id)

        logging.info("0000000:Encomenda._get_encomenda %s", encomenda)

        # Retorna uma resposta com status 200 (OK) e corpo contendo a encomenda.
        return jsonify(SchemaUtils.serialize(EncomendaEditSchema(), encomenda)), 200

    def put(self, encomenda_id):
        """
        Atualiza um recurso existente com todos os campos fornecidos.

        Recomendações para o uso do método PUT:
            - Inclua todos os campos do recurso, mesmo aqueles que não serão modificados.
            - Use valores mascarados para campos sensíveis que não devem ser alterados.
        """

        encomenda_data = request.get_json()

        nova_encomenda = SchemaUtils.deserialize(EncomendaEditSchema(), encomenda_data)

        logging.info("0: EncomendaApi.PUT: %s ", nova_encomenda)
        logging.info("1: EncomendaApi.PUT: %s ", nova_encomenda.status_encomenda)

        # Actualiza o usuário no banco de dados, junto com a nova pessoa associada
        self.encomenda_service.update(nova_encomenda, encomenda_id)

        # gera a resposta HATEOAS.
        hateoas_response_data = self.hateos_link_generator.generate_response(
            encomenda_id
        )

        # Retorna uma resposta com status 200 (OK) e corpo contendo os links HATEOAS.
        return jsonify(hateoas_response_data), 200

    def patch(self, encomenda_id):
        """
        Método PATCH: Actualiza parcialmente um recurso existente.
        Recomenda-se:
            - Obter apenas os campos que precisam ser atualizados (e não a representação completa do recurso).
            - Modificar apenas os campos especificados na solicitação.
            - Enviar a requisição PATCH com os campos atualizados para o servidor.
            - Implementar lógica para atualizar apenas os campos fornecidos, evitando a sobrescrição dos campos não mencionados.
        """

        if request.path.endswith("/cancel"):
            return self._patch_status(encomenda_id)

    def _patch_status(self, encomenda_id):

        self.encomenda_service.cancelar(encomenda_id)

        # Retorna uma resposta com status 204 (No Contect) indicando que o status foi
        # actualizado com sucesso.
        return "", 204
