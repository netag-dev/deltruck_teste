# statusEncomendaRepository.py

from app.extensions import db

from app.utils import BaseRepository

from .statusEncomenda import StatusEncomenda


class StatusEncomendaRepository(BaseRepository):
    def __init__(self):
        super().__init__(StatusEncomenda)

    def find_by_codigo(self, codigo):
        status_encomenda = (
            db.session.query(StatusEncomenda).filter_by(codigo=codigo).first()
        )
        return status_encomenda
