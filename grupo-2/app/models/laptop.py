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
    stock_minimo = Column(Integer, nullable=False, default=5)
    descripcion = Column(Text, nullable=True)

    categoria_id = Column(Integer, ForeignKey("categoria.id"), nullable=False)
    marca_id = Column(Integer, ForeignKey("marca.id"), nullable=False)

    categoria = relationship("Categoria", backref="laptops")
    marca = relationship("Marca", backref="laptops")

    def stock_disponible(self, cantidad):
        return self.stock >= cantidad

    def reducir_stock(self, cantidad):
        if not self.stock_disponible(cantidad):
            raise ValueError(f"Stock insuficiente para {self}. Disponible: {self.stock}, solicitado: {cantidad}")
        self.stock -= cantidad

    def restaurar_stock(self, cantidad):
        self.stock += cantidad

    @property
    def stock_bajo(self):
        return self.stock <= self.stock_minimo

    def __repr__(self):
        return f"{self.marca} {self.modelo}"
