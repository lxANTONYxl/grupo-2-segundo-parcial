from flask import jsonify
from flask_appbuilder import BaseView, expose
from app.extensions import db
from app.models.laptop import Laptop
from app.models.detalle_pedido import DetallePedido
from app.models.pedido import Pedido
from app.utils.gemini import consultar_gemini
import json


class ReporteTopView(BaseView):

    @expose("/", methods=["GET"])
    def list(self):
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

    @expose("/pronostico/", methods=["GET"])
    def pronostico(self):
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
        top_txt = "\n".join(
            f"- {row[0].marca} {row[0].modelo}: {int(row[1])} unidades vendidas, "
            f"Bs. {float(row[2]):.2f} en ingresos"
            for row in top_laptops
        ) or "Sin datos"

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
        meses_txt = "\n".join(
            f"- {row[0]}: Bs. {float(row[1]):.2f}" for row in ingresos_mes
        ) or "Sin datos"

        prompt = f"""Eres un analista de ventas para una tienda de laptops en Bolivia.
Analiza los siguientes datos de ventas:

TOP 10 laptops más vendidas:
{top_txt}

Ingresos mensuales (pedidos no cancelados):
{meses_txt}

Con base en estos datos:
1. Identifica tendencias de venta (productos estrella, meses de mayor ingreso).
2. Pronostica qué modelos seguirán siendo populares el próximo mes.
3. Sugiere estrategias para aumentar ingresos.
Responde en español, de forma clara y concisa (máximo 200 palabras)."""

        resultado = consultar_gemini(prompt)
        return jsonify({"pronostico": resultado})