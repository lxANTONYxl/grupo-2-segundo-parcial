from flask_appbuilder import ModelView
from flask_appbuilder.models.sqla.interface import SQLAInterface
from app.models.marca import Marca


class MarcaView(ModelView):
    datamodel = SQLAInterface(Marca)

    list_title = "Marcas"
    add_title = "Agregar Marca"
    edit_title = "Editar Marca"

    list_columns = ["nombre", "pais_origen"]
    add_columns = ["nombre", "pais_origen"]
    edit_columns = ["nombre", "pais_origen"]
    show_columns = ["nombre", "pais_origen"]