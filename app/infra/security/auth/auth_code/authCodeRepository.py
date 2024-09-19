# authCodeRepository.py.py

from app.extensions import db

from app.utils import BaseRepository

from .authCode import AuthCode


class AuthCodeRepository(BaseRepository):
    def __init__(self):
        super().__init__(AuthCode)

    def find_by_code(self, code):
        return db.session.query(AuthCode).filter_by(code=code).one_or_none()
