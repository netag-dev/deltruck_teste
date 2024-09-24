# authViews.py

import logging

# from flasgger import swag_from
from flask import current_app
from flask import request, jsonify, json
from flask_jwt_extended import decode_token
from flask.views import MethodView
from werkzeug.exceptions import Forbidden

from datetime import datetime, timezone

from app.utils.schemaUtils import SchemaUtils

from app.infra.security.token import TokenService
from app.infra.security.auth import AuthService
from app.infra.security.auth.shemas import UserLoginSchema, AuthResponseSchema
from app.infra.email.emailService import EmailService

from app.infra.security.auth.auth_code.authCode import AuthCode
from app.infra.security.auth.auth_code.authCodeService import AuthCodeService
from app.utils.dateUtils import DateUtils

from .auth_code.authCodeService import AuthCodeService


class AuthApi(MethodView):
    def __init__(self):
        self.token_service = TokenService()
        self.auth_service = AuthService()
        self.user_login_schema = UserLoginSchema()
        self.auth_code_service = AuthCodeService()
        self.auth_response_schema = AuthResponseSchema()
        self.email_service = EmailService()
        self.auth_code_service = AuthCodeService()

    def post(self):
        if request.path.endswith("/login"):
            return self._post_login()
        elif request.path.endswith("/final-user"):
            return self._post_login()

        elif request.path.endswith("/final-user/send-email-verification"):
            return self._post_send_email_verification_code()

        else:
            return self._post_logout()

    def _post_login(self):
        """Método POST para login."""

        user_login_data = request.get_json()

        user = SchemaUtils.deserialize(UserLoginSchema(), user_login_data)

        # Autenticar o usuário

        user_auth = self.auth_service.authenticate_user(user.user_email, user.password)

        # Gerar o token para o usuário autenticado
        # O cliente pode usar uma biblioteca como 'jwt-decode' para ler o conteúdo do JWT,
        # como 'user_name', 'role_name' e a data de 'expiração'.
        # O cliente pode verificar se o token expirou e, se necessário, solicitar um novo login.
        # A assinatura do token, gerada com a chave privada do servidor, não pode ser decodificada pelo cliente,
        # mas pode ser verificada com a chave pública distribuida pelo servidor para garantir que o token é autêntico e não foi alterado.
        # Quando o cliente precisa fazer uma requisição autenticada, ele deve recuperar o token do 'localStorage' e configurá-lo no cabeçalho Authorization com o prefixo "Bearer".
        # Ex.,const headers = { "Authorization": `Bearer ${token}`};
        access_token = self.token_service.generate_token(
            user_auth.id, user_auth.user_email, user_auth.role.name
        )

        logging.info("0: LoginApi.post")

        # Decodificar o token para obter informações
        decoded_token = decode_token(access_token)
        exp_timestamp = decoded_token["exp"]
        iat_timestamp = decoded_token["iat"]

        # Converter timestamps para datas legíveis
        iat_date = datetime.fromtimestamp(iat_timestamp, tz=timezone.utc)
        exp_date = datetime.fromtimestamp(exp_timestamp, tz=timezone.utc)

        # Logar as datas
        logging.info("Token Issuance Date: %s", iat_date)
        logging.info("Token Expiration Date: %s", exp_date)

        auth_data = {
            "user_email": user_auth.user_email,
            "access_token": access_token,
            "role_name": user_auth.role.name,
        }

        # Retorna uma resposta com status 200 (OK) e corpo contendo o dados de autenticação
        return jsonify(self.auth_response_schema.dump(auth_data)), 200

    def _post_send_email_verification_code(self):

        data = request.get_json()

        auth_code_time = AuthCodeService.get_auth_code_expiration_time()

        user_email = data.get("user_email")
        primeiro_nome = data.get("primeiro_nome")
        ultimo_nome = data.get("ultimo_nome")

        code = AuthCodeService.generate_auth_code()
        subject = "Confirmação do endereço de e-mail"
        recipients = user_email

        auth_code = AuthCode(code=code, expiration_time=auth_code_time)
        auth_code_criado = self.auth_code_service.create(auth_code)

        logging.info("0: AuthApi.post_generate_auth_code(): %s", auth_code_criado)

        body = (
            f"Obrigado por verificar sua conta, {primeiro_nome} {ultimo_nome},<br><br>"
            f"<strong>Seu código é: {code}</strong><br><br>"
        )

        logging.info("1: AuthApi()._post_user_final:  auth code: %s", code)
        logging.info("2: AuthApi()._post_user_final:  auth code: %s", auth_code_criado)

        self.email_service.send_email(subject, recipients, body)

        logging.info("3: AuthApi()._post_user_final")

        # Retorna uma resposta com status 204 (No Contect) indicando que o email foi
        # enviado com sucesso.
        return "", 204

    def get(self):
        if request.path.endswith("/auth-code-verification"):
            return self._get_auth_code_verification()

    def _get_auth_code_verification(self):
        data = request.get_json()

        logging.info("1: AuthApi()._get_auth_code_verification:  auth code")
        auth_code = data.get("auth_code")

        self.auth_code_service.get_by_code(auth_code.upper())
        logging.info("1: AuthApi()._get_auth_code_verification")

        # Retorna uma resposta com status 204 (No Content) indicando que a verificação do código foi bem-sucedida
        return "", 204

    def _post_logout(self):
        pass
