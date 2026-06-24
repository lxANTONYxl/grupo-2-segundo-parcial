from flask_appbuilder import BaseView, expose
from app.extensions import db
from app.models.laptop import Laptop
from app.models.pedido import Pedido
from app.models.detalle_pedido import DetallePedido
from app.models.cliente import Cliente
from app.models.categoria import Categoria
import json
import datetime


class DashboardView(BaseView):
    
    default_view = "index"

    @expose("/")
    def index(self):
        total_laptops = db.session.query(db.func.count(Laptop.id)).scalar() or 0
        total_ventas = (
            db.session.query(db.func.count(Pedido.id))
            .filter(Pedido.estado.in_(["Confirmado", "Enviado", "Entregado"]))
            .scalar() or 0
        )
        total_clientes = db.session.query(db.func.count(Cliente.id)).scalar() or 0
        stock_bajo = (
            db.session.query(db.func.count(Laptop.id))
            .filter(Laptop.stock <= Laptop.stock_minimo)
            .filter(Laptop.stock > 0)
            .scalar() or 0
        )
        sin_stock = (
            db.session.query(db.func.count(Laptop.id))
            .filter(Laptop.stock <= 0)
            .scalar() or 0
        )

        ingresos_totales = (
            db.session.query(db.func.coalesce(db.func.sum(Pedido.total), 0))
            .filter(Pedido.estado.in_(["Confirmado", "Enviado", "Entregado"]))
            .scalar() or 0
        )

        pedidos_recientes = (
            db.session.query(Pedido)
            .order_by(Pedido.fecha.desc(), Pedido.id.desc())
            .limit(5)
            .all()
        )

        laptops_stock_bajo = (
            db.session.query(Laptop)
            .filter(Laptop.stock <= Laptop.stock_minimo)
            .order_by(Laptop.stock.asc())
            .all()
        )

        ingresos_mes = (
            db.session.query(
                db.func.date_format(Pedido.fecha, "%Y-%m").label("mes"),
                db.func.coalesce(db.func.sum(Pedido.total), 0).label("ingresos"),
            )
            .filter(Pedido.estado.in_(["Confirmado", "Enviado", "Entregado"]))
            .group_by("mes")
            .order_by("mes")
            .all()
        )

        ventas_categoria = (
            db.session.query(
                Categoria.nombre,
                db.func.coalesce(db.func.count(DetallePedido.id), 0).label("total"),
            )
            .select_from(Categoria)
            .outerjoin(Laptop, Laptop.categoria_id == Categoria.id)
            .outerjoin(DetallePedido, DetallePedido.laptop_id == Laptop.id)
            .outerjoin(Pedido, Pedido.id == DetallePedido.pedido_id)
            .filter(
                Pedido.estado.in_(["Confirmado", "Enviado", "Entregado"])
                | Pedido.estado.is_(None)
            )
            .group_by(Categoria.id)
            .all()
        )

        labels_mes = [r[0] for r in ingresos_mes]
        valores_mes = [float(r[1]) for r in ingresos_mes]

        labels_cat = [r[0] for r in ventas_categoria]
        valores_cat = [int(r[1]) for r in ventas_categoria]

        return self.render_template(
            "dashboard/dashboard.html",
            total_laptops=total_laptops,
            total_ventas=total_ventas,
            total_clientes=total_clientes,
            stock_bajo=stock_bajo,
            sin_stock=sin_stock,
            ingresos_totales=ingresos_totales,
            pedidos_recientes=pedidos_recientes,
            laptops_stock_bajo=laptops_stock_bajo,
            labels_mes=json.dumps(labels_mes),
            valores_mes=json.dumps(valores_mes),
            labels_cat=json.dumps(labels_cat),
            valores_cat=json.dumps(valores_cat),
        )
