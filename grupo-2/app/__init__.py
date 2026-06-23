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
        from app.views.reportes.reporte_ventas import ReporteVentasView
        from app.views.reportes.reporte_top import ReporteTopView
        
        appbuilder.add_view(
            CategoriaView, "Categorías", icon="fa-tags", category="Catálogo"
        )
        appbuilder.add_view(
            MarcaView, "Marcas", icon="fa-trademark", category="Catálogo"
        )
        appbuilder.add_view(
            LaptopView, "Laptops", icon="fa-laptop", category="Catálogo"
        )
        
        appbuilder.add_view(
            ClienteView, "Clientes", icon="fa-users", category="Ventas"
        )
        appbuilder.add_view(
            PedidoView, "Pedidos", icon="fa-shopping-cart", category="Ventas"
        )
        appbuilder.add_view(
            DetallePedidoView,
            "Detalle de Pedidos",
            icon="fa-list",
            category="Ventas",
        )

        appbuilder.add_view(
            ReporteLaptopsView,
            "Laptops por Categoría",
            icon="fa-chart-bar",
            category="Reportes",
        )
        
        appbuilder.add_view(
            ReporteVentasView,
            "Ventas por Cliente",
            icon="fa-chart-pie",
            category="Reportes",
        )
        
        appbuilder.add_view(
            ReporteTopView,
            "Top Laptops Vendidas",
            icon="fa-chart-line",
            category="Reportes",
        )

        _configurar_roles(appbuilder)

    return app


# Permisos base que FAB necesita para que cualquier usuario pueda
# navegar: home, perfil, cambio de idioma, y la API del menú lateral.
PERMISOS_BASE = [
    ("can_get", "CurrentUserRestApi"),
    ("can_info", "CurrentUserRestApi"),
    ("can_index", "IndexView"),
    ("can_get", "OpenApi"),
    ("can_show", "SwaggerView"),
    ("can_this_form_get", "ResetMyPasswordView"),
    ("can_this_form_post", "ResetMyPasswordView"),
    ("can_this_form_get", "UserInfoEditView"),
    ("can_this_form_post", "UserInfoEditView"),
    ("can_userinfo", "UserDBModelView"),
    ("can_get", "MenuApi"),
    ("resetmypassword", "UserDBModelView"),
    ("userinfoedit", "UserDBModelView"),
]

PERMISOS_SUPERVISOR = PERMISOS_BASE + [
    # ── ACCESO VISUAL A MENÚS LATERALES ──────────────────────────────────────
    ("menu_access", "Catálogo"),
    ("menu_access", "Categorías"),
    ("menu_access", "Marcas"),
    ("menu_access", "Laptops"),
    ("menu_access", "Ventas"),
    ("menu_access", "Clientes"),
    ("menu_access", "Pedidos"),
    ("menu_access", "Detalle de Pedidos"),
    ("menu_access", "Reportes"),
    ("menu_access", "Laptops por Categoría"),
    ("menu_access", "Ventas por Cliente"),
    ("menu_access", "Top Laptops Vendidas"),
    # ── ACCIONES: Catálogo completo ──────────────────────────────────────────
    ("can_list", "CategoriaView"),
    ("can_show", "CategoriaView"),
    ("can_add", "CategoriaView"),
    ("can_edit", "CategoriaView"),
    ("can_delete", "CategoriaView"),
    ("can_list", "MarcaView"),
    ("can_show", "MarcaView"),
    ("can_add", "MarcaView"),
    ("can_edit", "MarcaView"),
    ("can_delete", "MarcaView"),
    ("can_list", "LaptopView"),
    ("can_show", "LaptopView"),
    ("can_add", "LaptopView"),
    ("can_edit", "LaptopView"),
    ("can_delete", "LaptopView"),
    # ── ACCIONES: Ventas completo ─────────────────────────────────────────────
    ("can_list", "ClienteView"),
    ("can_show", "ClienteView"),
    ("can_add", "ClienteView"),
    ("can_edit", "ClienteView"),
    ("can_delete", "ClienteView"),
    ("can_list", "PedidoView"),
    ("can_show", "PedidoView"),
    ("can_add", "PedidoView"),
    ("can_edit", "PedidoView"),
    ("can_delete", "PedidoView"),
    ("can_list", "DetallePedidoView"),
    ("can_show", "DetallePedidoView"),
    ("can_add", "DetallePedidoView"),
    ("can_edit", "DetallePedidoView"),
    ("can_delete", "DetallePedidoView"),
    # ── ACCIONES: Reportes ────────────────────────────────────────────────────
    ("can_list", "ReporteLaptopsView"),
    ("can_list", "ReporteVentasView"),
    ("can_list", "ReporteTopView"),
]

PERMISOS_USUARIO = PERMISOS_BASE + [
    # ── ACCESO VISUAL A MENÚS LATERALES ──────────────────────────────────────
    ("menu_access", "Catálogo"),
    ("menu_access", "Categorías"),
    ("menu_access", "Marcas"),
    ("menu_access", "Laptops"),
    ("menu_access", "Reportes"),
    ("menu_access", "Laptops por Categoría"),
    ("menu_access", "Ventas por Cliente"),
    ("menu_access", "Top Laptops Vendidas"),
    # ── ACCIONES: Catálogo solo lectura ──────────────────────────────────────
    ("can_list", "CategoriaView"),
    ("can_show", "CategoriaView"),
    ("can_list", "MarcaView"),
    ("can_show", "MarcaView"),
    ("can_list", "LaptopView"),
    ("can_show", "LaptopView"),
    # ── ACCIONES: Reportes solo lectura ──────────────────────────────────────
    ("can_list", "ReporteLaptopsView"),
    ("can_list", "ReporteVentasView"),
    ("can_list", "ReporteTopView"),
]


def _configurar_roles(appbuilder):
    _asignar_permisos_rol(appbuilder.sm, "Supervisor", PERMISOS_SUPERVISOR)
    _asignar_permisos_rol(appbuilder.sm, "Usuario", PERMISOS_USUARIO)


def _asignar_permisos_rol(sm, nombre_rol, lista_permisos):
    rol = sm.find_role(nombre_rol)
    if not rol:
        rol = sm.add_role(nombre_rol)

    for accion, vista in lista_permisos:
        pvm = sm.find_permission_view_menu(accion, vista)

        # Si el permiso de menú o vista no se encuentra registrado en la DB,
        # obligamos a FAB a crearlo en lugar de ignorarlo.
        if not pvm:
            pvm = sm.add_permission_view_menu(accion, vista)

        if pvm and pvm not in rol.permissions:
            sm.add_permission_role(rol, pvm)