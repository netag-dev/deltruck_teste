# encomendaService.py

import logging

from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from app.exceptions import EntityUniqueViolationException, EntityNotFoundException

from app.utils.singletonMeta import SingletonMeta

from .encomenda import Encomenda
from .encomendaRepository import EncomendaRepository
from app.domain.gest_encomendas.status_encomenda import StatusEncomendaService


class EncomendaService(metaclass=SingletonMeta):

    def __init__(self):
        self.encomenda_repository = EncomendaRepository()
        self.status_encomenda_service = StatusEncomendaService()

    def create(self, encomenda: Encomenda):
        try:
            id_status_encomenda = self.status_encomenda_service.get_by_nome(
                "Pendente"
            ).id

            encomenda.id_status_encomenda = id_status_encomenda

            encomenda_criado = self.encomenda_repository.save(encomenda)
            logging.info("1: EncomendaService.create(): %s", encomenda)
            return encomenda_criado

        except IntegrityError as ex:
            if "unique constraint" in str(ex.orig):
                logging.error("IntegrityError %s", ex.orig)
                raise EntityUniqueViolationException(ex.orig)

        except Exception as ex:
            logging.error("%s", ex)

    def get_all(self):
        return self.encomenda_repository.find_all()

    def get_by_id(self, encomenda_id):
        return self.encomenda_repository.find_by_id(encomenda_id)

    def update(self, nova_encomenda, encomenda_id):
        updated = self.encomenda_repository.update(nova_encomenda, encomenda_id)
        if updated is None:
            raise EntityNotFoundException(
                f"Encomenda com id {encomenda_id} não encontrado."
            )
        return updated

    def update_partial(self, encomenda_fields, id):
        return self.encomenda_repository.update_partial(encomenda_fields, id)

    def cancelar(self, id):
        status_encomenda_id = self.status_encomenda_service.get_by_nome("Cancelado").id
        encomenda_fields = {"id_status_encomenda": status_encomenda_id}
        return self.encomenda_repository.update_partial(encomenda_fields, id)
