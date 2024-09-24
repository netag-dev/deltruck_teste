# statusEncomenda.py

from sqlalchemy.orm import relationship

from app.extensions import db


class StatusEncomenda(db.Model):
    __tablename__ = "status_encomenda"
    __table_args__ = {"schema": "deltruck"}
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(
        db.String, nullable=False, unique=True
    )  # ex., Pendente, Em Trânsito, Cancelado, etc
    codigo = db.Column(
        db.String, nullable=False, unique=True
    )  # ex., pendente, em-transito, cancelado, etc
