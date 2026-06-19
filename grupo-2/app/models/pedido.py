from sqlalchemy import Column, Date, Float, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from app.extensions import db
import datetime


class Pedido(db.Model):
    __tablename__ = "pedido"

    id = Column(Integer, primary_key=True)
    fecha = Column(Date, nullable=False, default=datetime.date.today)
    total = Column(Float, nullable=False, default=0.0)
    estado = Column(String(50), nullable=False, default="Pendiente")  # Pendiente, Pagado, Cancelado

    # Relación con Cliente
    cliente_id = Column(Integer, ForeignKey("cliente.id"), nullable=False)
    cliente = relationship("Cliente", backref="pedidos")

    # Relación con detalles
    detalles = relationship("DetallePedido", back_populates="pedido", cascade="all, delete-orphan")

    def __repr__(self):
        return f"Pedido #{self.id} - {self.cliente}"