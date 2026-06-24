from flask import flash, redirect, request, url_for
from flask_appbuilder import BaseView, expose
from app.extensions import db
from app.models.cliente import Cliente
from app.models.laptop import Laptop
from app.models.pedido import Pedido
from app.models.detalle_pedido import DetallePedido
import datetime


class VentaView(BaseView):

    default_view = "nueva_venta"

    @expose("/", methods=["GET", "POST"])
    def nueva_venta(self):
        clientes = db.session.query(Cliente).order_by(Cliente.nombre).all()
        laptops = db.session.query(Laptop).order_by(Laptop.modelo).all()

        if request.method == "POST":
            cliente_id = request.form.get("cliente_id")
            laptop_ids = request.form.getlist("laptop_id[]")
            cantidades = request.form.getlist("cantidad[]")

            if not cliente_id:
                flash("Debe seleccionar un cliente", "danger")
                return self._render_form(clientes, laptops)

            cliente = db.session.get(Cliente, int(cliente_id))
            if not cliente:
                flash("Cliente no válido", "danger")
                return self._render_form(clientes, laptops)

            items = []
            for lid, cant in zip(laptop_ids, cantidades):
                if lid and cant:
                    laptop = db.session.get(Laptop, int(lid))
                    cantidad = int(cant)
                    if cantidad <= 0:
                        flash(f"Cantidad inválida para {laptop}", "danger")
                        return self._render_form(clientes, laptops)
                    if not laptop.stock_disponible(cantidad):
                        flash(
                            f"Stock insuficiente para {laptop}. "
                            f"Disponible: {laptop.stock}, solicitado: {cantidad}",
                            "danger",
                        )
                        return self._render_form(clientes, laptops)
                    items.append((laptop, cantidad))

            if not items:
                flash("Debe agregar al menos un producto", "danger")
                return self._render_form(clientes, laptops)

            pedido = Pedido(
                cliente=cliente,
                fecha=datetime.date.today(),
                total=0.0,
                estado="Confirmado",
            )
            db.session.add(pedido)
            db.session.flush()

            for laptop, cantidad in items:
                detalle = DetallePedido(
                    pedido=pedido,
                    laptop=laptop,
                    cantidad=cantidad,
                    precio_unitario=laptop.precio,
                    subtotal=cantidad * laptop.precio,
                )
                laptop.reducir_stock(cantidad)
                db.session.add(detalle)

            pedido.calcular_total()
            db.session.commit()

            flash(
                f"Venta #{pedido.id} creada con éxito para {cliente}",
                "success",
            )
            return redirect(url_for("VentaView.nueva_venta"))

        return self._render_form(clientes, laptops)

    def _render_form(self, clientes, laptops):
        return self.render_template(
            "venta/nueva_venta.html",
            clientes=clientes,
            laptops=laptops,
        )
