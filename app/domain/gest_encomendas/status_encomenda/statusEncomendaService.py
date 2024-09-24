# statusEncomendaService.py

import logging

from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from app.exceptions import EntityUniqueViolationException, EntityNotFoundException
from app.utils.singletonMeta import SingletonMeta

from .statusEncomendaRepository import StatusEncomendaRepository


class StatusEncomendaService(metaclass=SingletonMeta):

    def __init__(self):
        self.status_encomenda_repository = StatusEncomendaRepository()

    def get_all(self):
        return self.status_encomenda_repository.find_all()

    def get_by_codigo(self, codigo):
        status_encomenda = self.status_encomenda_repository.find_by_codigo(codigo)
        if status_encomenda is None:
            raise EntityNotFoundException(
                f"StatusEncomenda com id {codigo} não encontrado."
            )
        return status_encomenda
