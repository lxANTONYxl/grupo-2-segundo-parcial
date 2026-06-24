from flask_appbuilder import ModelView
from flask_appbuilder.models.sqla.interface import SQLAInterface
from app.models.laptop import Laptop


class LaptopView(ModelView):
    datamodel = SQLAInterface(Laptop)

    list_title = "Laptops"
    add_title = "Agregar Laptop"
    edit_title = "Editar Laptop"

    list_columns = [
        "marca", "modelo", "procesador", "ram_gb", "almacenamiento_gb",
        "precio", "stock", "stock_minimo", "categoria",
    ]
    add_columns = [
        "marca", "categoria", "modelo", "procesador", "ram_gb",
        "almacenamiento_gb", "precio", "stock", "stock_minimo", "descripcion",
    ]
    edit_columns = [
        "marca", "categoria", "modelo", "procesador", "ram_gb",
        "almacenamiento_gb", "precio", "stock", "stock_minimo", "descripcion",
    ]
    show_columns = [
        "marca", "categoria", "modelo", "procesador", "ram_gb",
        "almacenamiento_gb", "precio", "stock", "stock_minimo", "descripcion",
    ]

    label_columns = {
        "marca": "Marca",
        "categoria": "Categoría",
        "modelo": "Modelo",
        "procesador": "Procesador",
        "ram_gb": "RAM (GB)",
        "almacenamiento_gb": "Almacenamiento (GB)",
        "precio": "Precio (Bs.)",
        "stock": "Stock",
        "stock_minimo": "Stock Mínimo",
        "descripcion": "Descripción",
    }

    search_columns = ["modelo", "procesador", "marca", "categoria"]
