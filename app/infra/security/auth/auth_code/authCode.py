# authCode.py

from app.extensions import db


class AuthCode(db.Model):
    __tablename__ = "auth_code"
    __table_args__ = {"schema": "deltruck"}
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(8), nullable=False)
    expiration_time = db.Column(db.TIMESTAMP, nullable=False)
