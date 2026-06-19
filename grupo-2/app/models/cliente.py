from sqlalchemy import Column, Integer, String
from app.extensions import db


class Cliente(db.Model):
    __tablename__ = "cliente"

    id = Column(Integer, primary_key=True)
    nombre = Column(String(150), nullable=False)
    apellido = Column(String(150), nullable=False)
    email = Column(String(200), nullable=False, unique=True)
    telefono = Column(String(20), nullable=True)
    direccion = Column(String(300), nullable=True)

    def __repr__(self):
        return f"{self.nombre} {self.apellido}"