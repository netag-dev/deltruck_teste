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

    def get_by_nome(self, nome):
        return self.status_encomenda_repository.find_by_nome(nome)
