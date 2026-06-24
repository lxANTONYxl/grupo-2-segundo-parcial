from sqlalchemy import Column, Date, Float, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from app.extensions import db
from app.models.detalle_pedido import DetallePedido
import datetime


ESTADOS_PEDIDO = {
    "Pendiente": "Pendiente",
    "Confirmado": "Confirmado",
    "Enviado": "Enviado",
    "Entregado": "Entregado",
    "Cancelado": "Cancelado",
}


class Pedido(db.Model):
    __tablename__ = "pedido"

    id = Column(Integer, primary_key=True)
    fecha = Column(Date, nullable=False, default=datetime.date.today)
    total = Column(Float, nullable=False, default=0.0)
    estado = Column(String(50), nullable=False, default="Pendiente")
    observaciones = Column(String(500), nullable=True)

    cliente_id = Column(Integer, ForeignKey("cliente.id"), nullable=False)
    cliente = relationship("Cliente", backref="pedidos")

    detalles = relationship(
        "DetallePedido", back_populates="pedido", cascade="all, delete-orphan"
    )

    @property
    def items_count(self):
        return sum(d.cantidad for d in self.detalles)

    def calcular_total(self):
        self.total = sum(d.subtotal for d in self.detalles)

    def procesar_stock(self, accion):
        for detalle in self.detalles:
            laptop = detalle.laptop
            if accion == "reducir":
                laptop.reducir_stock(detalle.cantidad)
            elif accion == "restaurar":
                laptop.restaurar_stock(detalle.cantidad)

    def puede_confirmar(self):
        for detalle in self.detalles:
            if not detalle.laptop.stock_disponible(detalle.cantidad):
                return False
        return True

    def __repr__(self):
        return f"Pedido #{self.id} - {self.cliente}"
