from flask_appbuilder import ModelView
from flask_appbuilder.models.sqla.interface import SQLAInterface
from flask_appbuilder.security.decorators import has_access
from app.models.categoria import Categoria


class CategoriaView(ModelView):
    datamodel = SQLAInterface(Categoria)

    list_title = "Categorías"
    add_title = "Agregar Categoría"
    edit_title = "Editar Categoría"

    list_columns = ["nombre", "descripcion"]
    add_columns = ["nombre", "descripcion"]
    edit_columns = ["nombre", "descripcion"]
    show_columns = ["nombre", "descripcion"]

    add_exclude_columns = []
    edit_exclude_columns = []