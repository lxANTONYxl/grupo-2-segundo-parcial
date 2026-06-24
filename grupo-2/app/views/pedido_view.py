from flask import flash
from flask_appbuilder import ModelView
from flask_appbuilder.models.sqla.interface import SQLAInterface
from app.models.pedido import Pedido
from app.extensions import db


ESTADOS_PERMITIDOS = {
    "Pendiente": ["Confirmado", "Cancelado"],
    "Confirmado": ["Enviado", "Cancelado"],
    "Enviado": ["Entregado", "Cancelado"],
    "Entregado": [],
    "Cancelado": ["Pendiente"],
}


class PedidoView(ModelView):
    datamodel = SQLAInterface(Pedido)

    list_title = "Pedidos"
    add_title = "Registrar Pedido"
    edit_title = "Editar Pedido"

    list_columns = ["id", "cliente", "fecha", "total", "estado"]
    add_columns = ["cliente", "fecha", "estado", "observaciones"]
    edit_columns = ["cliente", "fecha", "estado", "observaciones"]
    show_columns = [
        "cliente", "fecha", "estado", "total", "observaciones", "detalles"
    ]

    label_columns = {
        "id": "N° Pedido",
        "cliente": "Cliente",
        "fecha": "Fecha",
        "total": "Total (Bs.)",
        "estado": "Estado",
        "detalles": "Detalle",
        "observaciones": "Observaciones",
    }

    search_columns = ["estado", "cliente"]

    def pre_add(self, item):
        item.estado = "Pendiente"

    def pre_update(self, item):
        old = self.datamodel.get(item.id)
        item._old_estado = old.estado if old else item.estado

        if old and old.estado != item.estado:
            transiciones = ESTADOS_PERMITIDOS.get(old.estado, [])
            if item.estado not in transiciones:
                flash(
                    f"No se puede cambiar de '{old.estado}' a '{item.estado}'. "
                    f"Transiciones permitidas: {', '.join(transiciones)}",
                    "danger",
                )
                return False

    def post_update(self, item):
        old_estado = getattr(item, '_old_estado', item.estado)
        new_estado = item.estado

        if old_estado != new_estado:
            if new_estado == "Cancelado" and old_estado != "Pendiente":
                try:
                    item.procesar_stock("restaurar")
                    flash("Stock restaurado correctamente", "success")
                except ValueError as e:
                    flash(str(e), "danger")
            elif old_estado == "Cancelado" and new_estado != "Cancelado":
                if item.puede_confirmar():
                    item.procesar_stock("reducir")
                    flash("Stock reducido correctamente", "success")
                else:
                    flash(
                        "No hay suficiente stock para confirmar este pedido",
                        "danger",
                    )
                    db.session.rollback()
                    return
            elif new_estado in ("Confirmado", "Enviado", "Entregado"):
                if item.puede_confirmar():
                    item.procesar_stock("reducir")
                    flash("Stock reducido correctamente", "success")
                else:
                    flash(
                        "No hay suficiente stock para confirmar este pedido",
                        "danger",
                    )
                    db.session.rollback()
                    return
        item.calcular_total()
        db.session.commit()
