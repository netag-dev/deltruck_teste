# LocEncomendaService.py

import logging

from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from app.exceptions import EntityUniqueViolationException, EntityNotFoundException
from app.utils.singletonMeta import SingletonMeta

from .locEncomendaRepository import LocEncomendaRepository
from .locEncomenda import LocEncomenda


class LocEncomendaService(metaclass=SingletonMeta):

    def __init__(self):
        self.loc_encomenda_repository = LocEncomendaRepository()

    def create(self, loc_encomenda: LocEncomenda):
        try:
            logging.debug("0: LocEncomendaService().create()")

            logging.debug("1: LocEncomendaService().create()")
            loc_encomenda_criado = self.loc_encomenda_repository.save(loc_encomenda)

            logging.info("2: LocEncomendaService.create()")
            return loc_encomenda_criado

        except Exception as ex:
            logging.error("%s", ex)
            raise

    def update_encomenda_location(self, nova_loc_encomenda):
        return self.create(nova_loc_encomenda)
