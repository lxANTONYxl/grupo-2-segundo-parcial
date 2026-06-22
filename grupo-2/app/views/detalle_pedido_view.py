from flask_appbuilder import ModelView
from flask_appbuilder.models.sqla.interface import SQLAInterface
from app.models.detalle_pedido import DetallePedido


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