from flask_appbuilder import BaseView, expose
from app.extensions import db
from app.models.laptop import Laptop
from app.models.detalle_pedido import DetallePedido
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

        # Labels y valores para gráfica de barras horizontal
        labels_top = [f"{row[0].marca} {row[0].modelo}" for row in top_laptops]
        valores_top = [int(row[1]) for row in top_laptops]

        return self.render_template(
            "reportes/reporte_top.html",
            top_laptops=top_laptops,
            labels_top=json.dumps(labels_top),
            valores_top=json.dumps(valores_top),
        )