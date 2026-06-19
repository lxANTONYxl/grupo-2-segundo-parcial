from sqlalchemy import Column, Float, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship
from app.extensions import db


class Laptop(db.Model):
    __tablename__ = "laptop"

    id = Column(Integer, primary_key=True)
    modelo = Column(String(150), nullable=False)
    procesador = Column(String(100), nullable=False)
    ram_gb = Column(Integer, nullable=False)
    almacenamiento_gb = Column(Integer, nullable=False)
    precio = Column(Float, nullable=False)
    stock = Column(Integer, nullable=False, default=0)
    descripcion = Column(Text, nullable=True)

    # Relaciones
    categoria_id = Column(Integer, ForeignKey("categoria.id"), nullable=False)
    marca_id = Column(Integer, ForeignKey("marca.id"), nullable=False)

    categoria = relationship("Categoria", backref="laptops")
    marca = relationship("Marca", backref="laptops")

    def __repr__(self):
        return f"{self.marca} {self.modelo}"