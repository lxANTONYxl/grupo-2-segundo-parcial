from flask import request, jsonify
from flask_appbuilder import BaseView, expose
from app.extensions import db
from app.models.cliente import Cliente
from app.models.pedido import Pedido
from app.utils.gemini import consultar_gemini


class ReporteVentasView(BaseView):

    @expose("/", methods=["GET"])
    def list(self):
        clientes = db.session.query(Cliente).all()
        cliente_id_sel = request.args.get("cliente_id", "")

        datos_grafica = (
            db.session.query(
                (Cliente.nombre + " " + Cliente.apellido).label("nombre_completo"),
                db.func.coalesce(db.func.sum(Pedido.total), 0).label("total"),
            )
            .outerjoin(Pedido, Pedido.cliente_id == Cliente.id)
            .group_by(Cliente.id)
            .all()
        )
        labels = [row[0] for row in datos_grafica]
        valores = [float(row[1]) for row in datos_grafica]

        pedidos = []
        cliente_nombre = ""
        total_cliente = 0.0
        if cliente_id_sel:
            pedidos = (
                db.session.query(Pedido)
                .filter(Pedido.cliente_id == int(cliente_id_sel))
                .order_by(Pedido.fecha.desc())
                .all()
            )
            cliente_obj = db.session.get(Cliente, int(cliente_id_sel))
            if cliente_obj:
                cliente_nombre = f"{cliente_obj.nombre} {cliente_obj.apellido}"
            total_cliente = sum(p.total for p in pedidos)

        return self.render_template(
            "reportes/reporte_ventas.html",
            clientes=clientes,
            cliente_id_sel=cliente_id_sel,
            pedidos=pedidos,
            cliente_nombre=cliente_nombre,
            total_cliente=total_cliente,
            labels=labels,
            valores=valores,
        )

    @expose("/pronostico/", methods=["GET"])
    def pronostico(self):
        datos_grafica = (
            db.session.query(
                (Cliente.nombre + " " + Cliente.apellido).label("nombre_completo"),
                db.func.coalesce(db.func.sum(Pedido.total), 0).label("total"),
                db.func.count(Pedido.id).label("num_pedidos"),
            )
            .outerjoin(Pedido, Pedido.cliente_id == Cliente.id)
            .group_by(Cliente.id)
            .order_by(db.desc("total"))
            .all()
        )
        clientes_txt = "\n".join(
            f"- {row[0]}: Bs. {float(row[1]):.2f} en {int(row[2])} pedido(s)"
            for row in datos_grafica
        ) or "Sin datos"

        prompt = f"""Eres un analista de clientes para una tienda de laptops en Bolivia.
Analiza los siguientes datos de ventas por cliente:

{clientes_txt}

Con base en estos datos:
1. Identifica los clientes más valiosos (mayor gasto total).
2. Detecta clientes inactivos o con bajo consumo que podrían necesitar atención.
3. Pronostica el comportamiento de compra del próximo mes y sugiere estrategias de fidelización.
Responde en español, de forma clara y concisa (máximo 200 palabras)."""

        resultado = consultar_gemini(prompt)
        return jsonify({"pronostico": resultado})