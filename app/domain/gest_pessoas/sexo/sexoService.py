# sexoService.py

from app.utils.singletonMeta import SingletonMeta

from .sexo import Sexo
from .sexoRepository import SexoRepository


class SexoService(metaclass=SingletonMeta):
    def __init__(self):
        self.sexo_repository = SexoRepository()

    def get_all(self):
        return self.sexo_repository.find_all()

    def get_by_nome(self, nome):
        return self.sexo_repository.find_by_nome(nome)
