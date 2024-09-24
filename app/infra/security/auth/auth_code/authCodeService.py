# authCodeService.py
import secrets, logging
from datetime import datetime, timedelta, timezone
from flask import current_app

from app.utils.singletonMeta import SingletonMeta

from app.exceptions.entityNotFoundException import EntityNotFoundException

from .authCodeRepository import AuthCodeRepository
from .authCode import AuthCode


class AuthCodeService(metaclass=SingletonMeta):
    def __init__(self):
        self.auth_code_repository = AuthCodeRepository()

    def create(self, auth_code: AuthCode):
        logging.debug("0: AuthCodeService().create()")

        logging.debug("1: AuthCodeService().create()")
        auth_code_criado = self.auth_code_repository.save(auth_code)

        logging.info("2: AuthCodeService.create()")
        return auth_code_criado

    def get_by_code(self, code):
        auth = self.auth_code_repository.find_by_code(code)
        if auth is None:
            raise EntityNotFoundException(f"AuthCode: {code} não encontrado.")
        return auth

    def get_by_code(self, code):
        auth = self.auth_code_repository.find_by_code(code)
        if auth is None:
            raise EntityNotFoundException(f"AuthCode: {code} não encontrado.")
        return auth

    def delete(self, id):
        return self.auth_code_repository.delete(id)

    def delete_by_code(self, code):
        auth_code = self.get_by_code(code)
        self.delete(auth_code.id)

    def is_auth_code_valid(self, auth_code):
        auth_code = self.get_by_code(auth_code)

        current_time = datetime.now()

        # Converte auth.expiration_time para datetime com a data atual
        expiration_datetime = datetime.combine(
            current_time.date(), auth.expiration_time
        )

        if current_time < expiration_datetime:
            return auth_code
        else:
            return None

    @staticmethod
    def get_auth_code_expiration_time():
        emission_time = datetime.now(timezone.utc)
        expiration_seconds = current_app.config.get("AUTH_CODE_EXPIRATION")
        # Calcula o tempo exato em que o codigo vai expirar:
        # Exemplo: '2024-08-18 14:30:00' + timedelta(15) => 2024-08-18 14:45:00'
        expiration_time = datetime.now(timezone.utc) + timedelta(
            seconds=expiration_seconds
        )
        logging.info(
            "AuthCodeService.0 get_auth_code_expiration_time: emission_time : %s",
            emission_time,
        )
        logging.info(
            "AuthCodeService.1 get_auth_code_expiration_time: expiration_time : %s",
            expiration_time,
        )

        return expiration_time

    @staticmethod
    def generate_auth_code():
        # Gera um código hexadecimal de 8 caracteres
        return secrets.token_hex(4).upper()
