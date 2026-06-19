from sqlalchemy import Column, Integer, String
from app.extensions import db


class Marca(db.Model):
    __tablename__ = "marca"

    id = Column(Integer, primary_key=True)
    nombre = Column(String(100), nullable=False, unique=True)
    pais_origen = Column(String(100), nullable=True)

    def __repr__(self):
        return self.nombre