# statusEncomendaViews.py

from flask import request, jsonify, json

from app.utils import BaseProtectedView, SchemaUtils
from app.domain.gest_encomendas.status_encomenda.schemas import (
    StatusEncomendaResponseSchema,
)
from . import StatusEncomendaService


class StatusEncomendaApi(BaseProtectedView):
    def __init__(self):
        super().__init__()
        self.status_encomenda_service = StatusEncomendaService()

    def get(self, status_encomenda_id=None):
        if status_encomenda_id is None:
            return self._get_all()

    def _get_all(self):
        """ """
        status_encomendas = self.status_encomenda_service.get_all()
        # Retorna uma resposta com status 200 (OK) e corpo contendo a lista de status_encomendas
        return (
            jsonify(
                SchemaUtils.serialize(
                    StatusEncomendaResponseSchema(), status_encomendas
                )
            ),
            200,
        )
