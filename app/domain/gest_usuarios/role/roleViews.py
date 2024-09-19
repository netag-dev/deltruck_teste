# roleViews.py

from flask import request, jsonify, json
from flask.views import MethodView

from app.utils.schemaUtils import SchemaUtils

from . import RoleService
from .schemas import RoleResponseSchema


class RolesApi(MethodView):
    def __init__(self):
        super().__init__()
        self.role_service = RoleService()

    def get(self, role_id=None):
        if role_id is None:
            return self._get_all()

    def _get_all(self):
        """ """
        roles = self.role_service.get_all_except_user_and_root()
        # Retorna uma resposta com status 200 (OK) e corpo contendo a lista de roles
        return jsonify(SchemaUtils.serialize(RoleResponseSchema(), roles)), 200
