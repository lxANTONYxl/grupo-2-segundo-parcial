from flask import flash
from flask_appbuilder import ModelView
from flask_appbuilder.models.sqla.interface import SQLAInterface
from app.models.detalle_pedido import DetallePedido
from app.extensions import db


class DetallePedidoView(ModelView):
    datamodel = SQLAInterface(DetallePedido)

    list_title = "Detalles de Pedidos"
    add_title = "Agregar Detalle"
    edit_title = "Editar Detalle"

    list_columns = ["pedido", "laptop", "cantidad", "precio_unitario", "subtotal"]
    add_columns = ["pedido", "laptop", "cantidad", "precio_unitario", "subtotal"]
    edit_columns = ["pedido", "laptop", "cantidad", "precio_unitario", "subtotal"]
    show_columns = ["pedido", "laptop", "cantidad", "precio_unitario", "subtotal"]

    label_columns = {
        "pedido": "Pedido",
        "laptop": "Laptop",
        "cantidad": "Cantidad",
        "precio_unitario": "Precio unitario (Bs.)",
        "subtotal": "Subtotal (Bs.)",
    }

    def pre_add(self, item):
        laptop = item.laptop
        if not laptop.stock_disponible(item.cantidad):
            flash(
                f"Stock insuficiente para {laptop}. "
                f"Disponible: {laptop.stock}, solicitado: {item.cantidad}",
                "danger",
            )
            return False
        item.precio_unitario = laptop.precio
        item.subtotal = item.cantidad * item.precio_unitario

    def post_add(self, item):
        if item.pedido.estado in ("Confirmado", "Enviado", "Entregado"):
            try:
                item.laptop.reducir_stock(item.cantidad)
            except ValueError as e:
                flash(str(e), "danger")
                db.session.rollback()
                return
        item.pedido.calcular_total()
        db.session.commit()

    def pre_update(self, item):
        old = self.datamodel.get(item.id)
        item._old_cantidad = old.cantidad if old else item.cantidad
        item._old_estado = old.pedido.estado if old else item.pedido.estado

        if old and old.cantidad != item.cantidad:
            laptop = item.laptop
            diff = item.cantidad - old.cantidad
            if diff > 0 and not laptop.stock_disponible(diff):
                flash(
                    f"Stock insuficiente para {laptop}. "
                    f"Disponible: {laptop.stock}, adicional necesario: {diff}",
                    "danger",
                )
                return False
        item.subtotal = item.cantidad * item.precio_unitario

    def post_update(self, item):
        if hasattr(item, '_old_cantidad') and item._old_cantidad != item.cantidad:
            diff = item.cantidad - item._old_cantidad
            laptop = item.laptop
            if item.pedido.estado not in ("Pendiente", "Cancelado"):
                if diff > 0:
                    laptop.reducir_stock(diff)
                else:
                    laptop.restaurar_stock(-diff)
        item.pedido.calcular_total()
        db.session.commit()

    def pre_delete(self, item):
        if item.pedido.estado not in ("Pendiente", "Cancelado"):
            flash(
                "Solo se pueden eliminar detalles de pedidos Pendientes o Cancelados",
                "danger",
            )
            return False

    def post_delete(self, item):
        if item.pedido.estado in ("Confirmado", "Enviado", "Entregado"):
            item.laptop.restaurar_stock(item.cantidad)
        item.pedido.calcular_total()
        db.session.commit()
