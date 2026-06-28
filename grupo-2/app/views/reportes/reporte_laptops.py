from flask import request, jsonify
from flask_appbuilder import BaseView, expose
from app.extensions import db
from app.models.categoria import Categoria
from app.models.laptop import Laptop
from app.utils.gemini import consultar_gemini


class ReporteLaptopsView(BaseView):

    @expose("/", methods=["GET"])
    def list(self):
        categorias = db.session.query(Categoria).all()
        cat_id_sel = request.args.get("cat_id", "")

        datos_grafica = (
            db.session.query(Categoria.nombre, db.func.count(Laptop.id))
            .join(Laptop, Laptop.categoria_id == Categoria.id, isouter=True)
            .group_by(Categoria.id)
            .all()
        )
        labels = [row[0] for row in datos_grafica]
        valores = [row[1] for row in datos_grafica]

        laptops = []
        categoria_nombre = ""
        if cat_id_sel:
            laptops = (
                db.session.query(Laptop)
                .filter(Laptop.categoria_id == int(cat_id_sel))
                .all()
            )
            cat_obj = db.session.get(Categoria, int(cat_id_sel))
            if cat_obj:
                categoria_nombre = cat_obj.nombre

        return self.render_template(
            "reportes/reporte_laptops.html",
            categorias=categorias,
            cat_id_sel=cat_id_sel,
            laptops=laptops,
            categoria_nombre=categoria_nombre,
            labels=labels,
            valores=valores,
        )

    @expose("/pronostico/", methods=["GET"])
    def pronostico(self):
        # Recopilar datos para el prompt
        datos_grafica = (
            db.session.query(Categoria.nombre, db.func.count(Laptop.id))
            .join(Laptop, Laptop.categoria_id == Categoria.id, isouter=True)
            .group_by(Categoria.id)
            .all()
        )
        resumen = "\n".join(
            f"- {row[0]}: {row[1]} laptop(s)" for row in datos_grafica
        )

        # Stock bajo
        laptops_bajo_stock = (
            db.session.query(Laptop)
            .filter(Laptop.stock <= Laptop.stock_minimo)
            .all()
        )
        bajo_stock_txt = "\n".join(
            f"  * {l.modelo} (stock: {l.stock}, mínimo: {l.stock_minimo})"
            for l in laptops_bajo_stock
        ) or "  Ninguna"

        prompt = f"""Eres un analista de inventario para una tienda de laptops en Bolivia.
Analiza los siguientes datos de stock por categoría:

{resumen}

Laptops con stock bajo o en nivel mínimo:
{bajo_stock_txt}

Con base en estos datos:
1. Identifica qué categorías tienen más y menos productos disponibles.
2. Da un pronóstico de cuáles categorías podrían quedarse sin stock próximamente.
3. Recomienda acciones concretas de reabastecimiento.
Responde en español, de forma clara y concisa (máximo 200 palabras)."""

        resultado = consultar_gemini(prompt)
        return jsonify({"pronostico": resultado})