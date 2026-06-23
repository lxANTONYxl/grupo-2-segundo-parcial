from flask_appbuilder import BaseView, expose
from app.extensions import db
from app.models.laptop import Laptop
from app.models.detalle_pedido import DetallePedido
from app.models.pedido import Pedido
import json


class ReporteTopView(BaseView):

    @expose("/", methods=["GET"])
    def list(self):
import json

class ReporteTopView(BaseView):
    """
    Reporte 3 (Integrante 3 - Antony):
    Muestra el ranking de laptops más vendidas (por cantidad)
    y una gráfica de línea con los ingresos totales por mes.
    """

    @expose("/", methods=["GET"])
    def list(self):
        # ── Top 10 laptops más vendidas ──────────────────────────────────────
        top_laptops = (
            db.session.query(
                Laptop,
                db.func.sum(DetallePedido.cantidad).label("total_vendido"),
                db.func.sum(DetallePedido.subtotal).label("total_ingresos"),
            )
            .join(DetallePedido, DetallePedido.laptop_id == Laptop.id)
            .group_by(Laptop.id)
            .order_by(db.desc("total_vendido"))
            .limit(10)
            .all()
        )

        labels_top = [f"{row[0].marca} {row[0].modelo}" for row in top_laptops]
        valores_top = [int(row[1]) for row in top_laptops]

        # Labels y valores para gráfica de barras horizontal
        labels_top = [f"{row[0].marca} {row[0].modelo}" for row in top_laptops]
        valores_top = [int(row[1]) for row in top_laptops]

        # ── Ingresos por mes (gráfica de línea) ─────────────────────────────
        ingresos_mes = (
            db.session.query(
                db.func.date_format(Pedido.fecha, "%Y-%m").label("mes"),
                db.func.sum(Pedido.total).label("ingresos"),
            )
            .filter(Pedido.estado != "Cancelado")
            .group_by("mes")
            .order_by("mes")
            .all()
        )

        labels_mes = [row[0] for row in ingresos_mes]
        valores_mes = [float(row[1]) for row in ingresos_mes]

        return self.render_template(
            "reportes/reporte_top.html",
            top_laptops=top_laptops,
            labels_top=json.dumps(labels_top),
            valores_top=json.dumps(valores_top),
            labels_mes=json.dumps(labels_mes),
            valores_mes=json.dumps(valores_mes),
        )