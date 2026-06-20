from flask_appbuilder import ModelView
from flask_appbuilder.models.sqla.interface import SQLAInterface
from app.models.cliente import Cliente


class ClienteView(ModelView):
    datamodel = SQLAInterface(Cliente)

    list_title = "Clientes"
    add_title = "Registrar Cliente"
    edit_title = "Editar Cliente"

    list_columns = ["nombre", "apellido", "email", "telefono"]
    add_columns = ["nombre", "apellido", "email", "telefono", "direccion"]
    edit_columns = ["nombre", "apellido", "email", "telefono", "direccion"]
    show_columns = ["nombre", "apellido", "email", "telefono", "direccion"]

    label_columns = {
        "nombre": "Nombre",
        "apellido": "Apellido",
        "email": "Correo electrónico",
        "telefono": "Teléfono",
        "direccion": "Dirección",
    }

    search_columns = ["nombre", "apellido", "email"]