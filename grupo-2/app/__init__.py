from flask import Flask

from .extensions import appbuilder, db


def create_app() -> Flask:
    app = Flask(__name__)
    app.config.from_object("config")
    
    db.init_app(app)
    
    with app.app_context():
        appbuilder.init_app(app, db.session)
        
        from app.models.categoria import Categoria
        from app.models.marca import Marca
        from app.models.laptop import Laptop
        from app.models.cliente import Cliente
        from app.models.pedido import Pedido
        from app.models.detalle_pedido import DetallePedido
        
        db.create_all()
        
        from app.views.categoria_view import CategoriaView
        from app.views.marca_view import MarcaView
        from app.views.laptop_view import LaptopView
        from app.views.cliente_view import ClienteView
        from app.views.pedido_view import PedidoView
        from app.views.detalle_pedido_view import DetallePedidoView
        from app.views.reportes.reporte_laptops import ReporteLaptopsView
        
        appbuilder.add_view(
            CategoriaView, "Categorías",
            icon="fa-tags", category="Catálogo"
        )
        appbuilder.add_view(
            MarcaView, "Marcas",
            icon="fa-trademark", category="Catálogo"
        )
        appbuilder.add_view(
            LaptopView, "Laptops",
            icon="fa-laptop", category="Catálogo"
        )
        
        appbuilder.add_view(
            ClienteView, "Clientes",
            icon="fa-users", category="Ventas"
        )
        appbuilder.add_view(
            PedidoView, "Pedidos",
            icon="fa-shopping-cart", category="Ventas"
        )
        appbuilder.add_view(
            DetallePedidoView, "Detalle de Pedidos",
            icon="fa-list", category="Ventas"
        )
        
        appbuilder.add_view(
            ReporteLaptopsView, "Laptops por Categoría",
            icon="fa-chart-bar", category="Reportes"
        )
        
        
        _crear_roles(appbuilder)
        
    return app


def _crear_roles(appbuilder):
    """Crea los roles Admin, Supervisor y Usuario si no existen."""
    from flask_appbuilder.security.sqla.models import Role

    roles_necesarios = ["Admin", "Supervisor", "Usuario"]
    roles_existentes = [r.name for r in appbuilder.sm.get_all_roles()]

    for nombre in roles_necesarios:
        if nombre not in roles_existentes:
            appbuilder.sm.add_role(nombre)
            