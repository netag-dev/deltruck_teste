# authService.py

import logging
from datetime import datetime, timezone

from app.utils.singletonMeta import SingletonMeta

from app.domain.gest_usuarios.user.userService import UserService
from app.infra.security.securityConfig import SecurityConfig

from .exceptions.invalidCredentialsException import InvalidCredentialsException
from .exceptions.invalidAuthCodeException import InvalidAuthCodeException

from .auth_code.authCodeService import AuthCodeService


class AuthService(metaclass=SingletonMeta):
    def __init__(self):
        self.user_service = UserService()
        self.auth_code_service = AuthCodeService()

    def authenticate_user(self, user_email, password):
        """Autenticação baseada em user_email e password"""

        logging.info("0: AuthService.authenticate_user()")

        user = self.user_service.get_user_by_user_email(user_email)
        logging.info("1: AuthService.authenticate_user(): %s", user)

        # Verifica se a password fornecida corresponde à password criptografada.
        if not SecurityConfig.check_password(user.password, password):
            raise InvalidCredentialsException("Credenciais inválidas.")
        return user

    def authenticate_user_with_two_factor(self, user_email, password, auth_code=None):
        """Autentica um usuário baseado em email, senha e código de autenticação (dois fatores)."""

        logging.debug("0: AuthService.authenticate_user_with_two_factor()")

        user = self.authenticate_user(user_email, password)

        if user.role.name != "USER":
            return None

        logging.debug("1: AuthService.authenticate_user_with_two_factor()")

        auth = self.auth_code_service.is_auth_code_valid(auth_code.upper())

        if auth_code and auth:
            logging.debug("2: AuthService.authenticate_user_with_two_factor()")
            self.auth_code_service.delete(auth.id)
            return user
        else:
            raise InvalidAuthCodeException(
                "Código de autenticação inválido ou Expirado."
            )
