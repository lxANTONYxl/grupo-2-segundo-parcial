from flask import request
from flask_appbuilder import BaseView, expose
from app.extensions import db
from app.models.cliente import Cliente
from app.models.pedido import Pedido


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
