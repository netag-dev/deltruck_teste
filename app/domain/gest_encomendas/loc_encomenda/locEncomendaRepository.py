# locEncomendaRepository.py

from app.extensions import db

from app.utils import BaseRepository

from .locEncomenda import LocEncomenda


class LocEncomendaRepository(BaseRepository):
    def __init__(self):
        super().__init__(LocEncomenda)
