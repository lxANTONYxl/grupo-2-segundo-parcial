from sqlalchemy import Column, Float, ForeignKey, Integer
from sqlalchemy.orm import relationship
from app.extensions import db


class DetallePedido(db.Model):
    __tablename__ = "detalle_pedido"

    id = Column(Integer, primary_key=True)
    cantidad = Column(Integer, nullable=False)
    precio_unitario = Column(Float, nullable=False)
    subtotal = Column(Float, nullable=False)

    # Relaciones
    pedido_id = Column(Integer, ForeignKey("pedido.id"), nullable=False)
    laptop_id = Column(Integer, ForeignKey("laptop.id"), nullable=False)

    pedido = relationship("Pedido", back_populates="detalles")
    laptop = relationship("Laptop", backref="detalles")

    def __repr__(self):
        return f"{self.cantidad}x {self.laptop}"