# statusEncomendaRepository.py

from app.extensions import db

from app.utils import BaseRepository

from .statusEncomenda import StatusEncomenda


class StatusEncomendaRepository(BaseRepository):
    def __init__(self):
        super().__init__(StatusEncomenda)

    def find_by_nome(self, nome):
        status_encoemnda = (
            db.session.query(StatusEncomenda).filter_by(nome=nome).first()
        )
        return status_encoemnda
