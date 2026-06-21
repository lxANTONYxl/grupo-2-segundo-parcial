from flask_appbuilder import ModelView
from flask_appbuilder.models.sqla.interface import SQLAInterface
from app.models.pedido import Pedido


class PedidoView(ModelView):
    datamodel = SQLAInterface(Pedido)

    list_title = "Pedidos"
    add_title = "Registrar Pedido"
    edit_title = "Editar Pedido"

    list_columns = ["id", "cliente", "fecha", "total", "estado"]
    add_columns = ["cliente", "fecha", "total", "estado"]
    edit_columns = ["cliente", "fecha", "total", "estado"]
    show_columns = ["cliente", "fecha", "total", "estado", "detalles"]

    label_columns = {
        "id": "N° Pedido",
        "cliente": "Cliente",
        "fecha": "Fecha",
        "total": "Total (Bs.)",
        "estado": "Estado",
        "detalles": "Detalle",
    }

    search_columns = ["estado", "cliente"]