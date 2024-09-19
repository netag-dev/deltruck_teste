# pessoaService.py.py

import logging

from sqlalchemy.exc import IntegrityError

from app.exceptions import EntityUniqueViolationException

from app.utils.baseRepository import BaseRepository
from app.utils.singletonMeta import SingletonMeta

from ..sexo import SexoService
from ..cidade import CidadeService
from ..contacto import ContactoService, Contacto
from ..endereco import EnderecoService, Endereco

from .pessoa import Pessoa
from .pessoaRepository import PessoaRepository

from ..sexo.sexoCache import SexoCache
from ..cidade.cidadeCache import CidadeCache


class PessoaService(metaclass=SingletonMeta):
    def __init__(self):
        self.pessoa_repository = PessoaRepository()
        self.contacto_service = ContactoService()
        self.endereco_service = EnderecoService()
        self.sexo_service = SexoService()
        self.cidade_service = CidadeService()
        self.sexo_data = SexoCache.get_sexo_cache()
        self.cidade_data = CidadeCache.get_cidade_cache()

    def create(self, pessoa: Pessoa):
        try:
            pessoa_criado = self.pessoa_repository.save(pessoa)
            logging.info("1: PessoaService.create(): %s", pessoa)
            return pessoa_criado

        except IntegrityError as ex:
            if "unique constraint" in str(ex.orig):
                logging.error("IntegrityError %s", ex.orig)
                raise EntityUniqueViolationException(ex.orig)

        except Exception as ex:
            logging.error("%s", ex)

    def create_pessoa_with_initial_details(self, pessoa: Pessoa):

        def transaction_function():

            id_sexo = self.sexo_service.get_by_nome("Não especificado").id
            id_cidade = self.cidade_service.get_by_nome("Não especificado").id

            contacto_criado = self.contacto_service.create(Contacto())

            endereco = Endereco()
            endereco.id_cidade = id_cidade

            endereco_criado = self.endereco_service.create(endereco)

            pessoa.id_sexo = id_sexo
            pessoa.contacto = contacto_criado
            pessoa.endereco = endereco_criado

            pessoa_criado = self.create(pessoa)

            logging.info("0: PessoaService.create_pessoa_with_initial_details()")

            return pessoa_criado

        return BaseRepository.transactional(transaction_function)
