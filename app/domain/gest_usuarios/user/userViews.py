# userViews.py

import logging

from flask import current_app
from flask import request, jsonify, json
from flask.views import MethodView
from flask_jwt_extended import jwt_required

from app.utils.schemaUtils import SchemaUtils
from app.utils.dateUtils import DateUtils

from app.utils.hateoasLinkGenerator import HateoasLinkGenerator

from app.infra.email.emailService import EmailService

from app.infra.security.authz.authorization import Authorization as authorization

from app.domain.gest_usuarios.user.userService import UserService
from app.domain.gest_usuarios.user.schemas import (
    UserCreateSchema,
    UserResponseSchema,
    UserEditScheme,
    UserEditPasswordSchema,
    FinalUserCreateSchema,
)

from app.domain.gest_pessoas.pessoa.pessoaService import PessoaService
from app.domain.gest_usuarios.role.roleService import RoleService
from app.domain.gest_pessoas.pessoa.schemas import PessoaCreateSchema

from app.infra.security.auth.auth_code.authCode import AuthCode
from app.infra.security.auth.auth_code.authCodeService import AuthCodeService


class UsersApi(MethodView):
    def __init__(self):
        super().__init__()
        self.user_service = UserService()
        self.role_service = RoleService()
        self.email_service = EmailService()
        self.auth_code_service = AuthCodeService()
        self.pessoa_service = PessoaService()
        self.hateos_link_generator = HateoasLinkGenerator(
            {
                "self": "users_api",
            },
            resource_id="user_id",
        )

    def post(self):
        if request.path.endswith("/final"):
            return self._post_user_final()
        else:
            return self._post_user()

    def _post_user(self):
        user_data = request.get_json()
        pessoa_data = user_data.pop("pessoa", None)

        pessoa = SchemaUtils.deserialize(PessoaCreateSchema(), pessoa_data)

        user = SchemaUtils.deserialize(UserCreateSchema(), user_data)

        # Associa a instância de Pessoa ao usuário
        # user.pessoa = pessoa

        # Cria o usuário no banco de dados, junto com a nova pessoa associada
        # user_criado = self.user_service.create(user)

        pessoa_criado = self.pessoa_service.create_pessoa_with_initial_details(pessoa)

        user.pessoa = pessoa_criado

        user_criado = self.user_service.create(user)

        logging.info("1: UsersApi.post")

        # retorna uma resposta com status 201 (CREATED) e corpo contendo os dados do usuário.
        return jsonify(SchemaUtils.serialize(UserResponseSchema(), user_criado)), 201

    def _post_user_final(self):
        user_data = request.get_json()
        pessoa_data = user_data.pop("pessoa", None)

        pessoa = SchemaUtils.deserialize(PessoaCreateSchema(), pessoa_data)

        user = SchemaUtils.deserialize(FinalUserCreateSchema(), user_data)

        logging.info("0: UsersApi()._post_user_final:")

        user.role = self.role_service.get_by_name("USER")
        user.pessoa = pessoa

        # Cria o usuário no banco de dados, junto com a nova pessoa associada
        user_criado = self.user_service.create(user)

        #
        auth_code_time = AuthCodeService.get_auth_code_expiration_time()

        code = AuthCodeService.generate_auth_code()
        subject = "Código de autenticação"
        recipients = user_criado.user_email

        auth_code = AuthCode(code=code, expiration_time=auth_code_time)
        auth_code_criado = self.auth_code_service.create(auth_code)

        auth_code_expire = current_app.config.get("AUTH_CODE_EXPIRATION")

        body = (
            f"Olá, {user_criado.pessoa.primeiro_nome} {user_criado.pessoa.ultimo_nome},\n\n"
            f"Seu código de autenticação é {code}\n\n"
            f"Este código é válido por {DateUtils.seconds_to_minutes(auth_code_expire)} minutos."
        )

        logging.info("0: UsersApi()._post_user_final:  auth code: %s", code)
        logging.info("1: UsersApi()._post_user_final:  auth code: %s", auth_code_criado)

        self.email_service.send_email(subject, recipients, body)

        # retorna uma resposta com status 201 (CREATED) e corpo contendo os dados do usuário.
        return jsonify(SchemaUtils.serialize(UserResponseSchema(), user_criado)), 201

    def get(self, user_id=None):
        if request.path.endswith("/final"):
            return self._get_all_final_users()
        if user_id is None:
            return self._get_all()
        else:
            return self._get_user(user_id)

    def _get_all(self):
        """ """
        users = self.user_service.get_all_except_role_user_and_root()
        # Retorna uma resposta com status 200 (OK) e corpo contendo a lista de usuários
        return jsonify(SchemaUtils.serialize(UserResponseSchema(), users)), 200

    def _get_all_final_users(self):
        """ """
        final_users = self.user_service.get_all_final_users()
        # Retorna uma resposta com status 200 (OK) e corpo contendo a lista de usuários finais
        return jsonify(SchemaUtils.serialize(UserResponseSchema(), final_users)), 200

    def _get_user(self, user_id):
        """ """
        user = self.user_service.get_by_id(user_id)

        # Retorna uma resposta com status 200 (OK) e corpo contendo o usuário.
        return jsonify(SchemaUtils.serialize(UserEditScheme(), user)), 200

    def put(self, user_id):
        """
        Atualiza um recurso existente com todos os campos fornecidos.

        Recomendações para o uso do método PUT:
            - Inclua todos os campos do recurso, mesmo aqueles que não serão modificados.
            - Use valores mascarados para campos sensíveis que não devem ser alterados.
        """

        user_data = request.get_json()

        novo_user = SchemaUtils.deserialize(UserEditScheme(), user_data)

        logging.info("0: UsersApi.PUT: %s ", novo_user)
        logging.info("1: UsersApi.PUT: %s ", novo_user.pessoa)

        # Actualiza o usuário no banco de dados, junto com a nova pessoa associada
        self.user_service.update(novo_user, user_id)

        # gera a resposta HATEOAS.
        hateoas_response_data = self.hateos_link_generator.generate_response(user_id)

        # Retorna uma resposta com status 200 (OK) e corpo contendo os links HATEOAS.
        return jsonify(hateoas_response_data), 200

    def patch(self, user_id):
        """
        Método PATCH: Actualiza parcialmente um recurso existente.
        Recomenda-se:
            - Obter apenas os campos que precisam ser atualizados (e não a representação completa do recurso).
            - Modificar apenas os campos especificados na solicitação.
            - Enviar a requisição PATCH com os campos atualizados para o servidor.
            - Implementar lógica para atualizar apenas os campos fornecidos, evitando a sobrescrição dos campos não mencionados.
        """

        if request.path.endswith("/update-password"):
            return self._patch_update_password(user_id)

        if request.path.endswith("/archived"):
            return self._patch_archive(user_id)

    def _patch_update_password(self, user_id):
        password_data = request.get_json()

        user_fields = SchemaUtils.deserialize(UserEditPasswordSchema(), password_data)

        self.user_service.update_partial(user_fields, user_id)

        # Retorna uma resposta com status 204 (No Contect) indicando que o usuário foi
        # actualizado com sucesso.
        return "", 204

    def _patch_archive(self, user_id):
        archived_status = request.args.get("archived")

        archived = archived_status.lower() in [
            "true",
            "yes",
            "1",
        ]  # Retorna 'True' se 'archived_status' for 'true', 'yes' ou '1'; caso contrário, retorna 'False'

        archived_field = {"archived": archived}

        self.user_service.update_partial(
            archived_field,
            user_id,
        )

        # Retorna uma resposta com status 204 (No Contect) indicando que o usuário foi
        # excluído com sucesso.
        return "", 204
