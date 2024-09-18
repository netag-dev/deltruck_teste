# userRepository.py

from sqlalchemy import desc, asc
from app.extensions import db

from app.utils import BaseRepository

from .user import User
from ..role import Role
from app.domain.gest_pessoas.pessoa import Pessoa


class UserRepository(BaseRepository):
    def __init__(self):
        super().__init__(User)

    def find_user_by_user_email(self, user_email):
        return db.session.query(User).filter_by(user_email=user_email).one_or_none()

    def find_all_except_role_user_and_root(self, archived=False):
        """Retorna todos os usuários, exceto aqueles com os papéis 'USER' e 'ROOT'."""
        return (
            db.session.query(User)
            .filter_by(archived=archived)
            .join(User.role)
            .join(User.pessoa)
            .filter(Role.name.notin_(["USER", "ROOT"]))
            .order_by(desc(User.id), asc(Pessoa.primeiro_nome))
            .all()
        )

    def find_all_by_role_user(self, archived=False):
        return (
            db.session.query(User)
            .filter_by(archived=archived)
            .join(User.role)
            .join(User.pessoa)
            .filter(Role.name.notin_(["ADMIN", "ROOT", "LOGISTA"]))
            .order_by(desc(User.id), asc(Pessoa.primeiro_nome))
            .all()
        )
