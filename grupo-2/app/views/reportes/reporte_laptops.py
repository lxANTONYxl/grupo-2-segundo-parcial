from flask import request
from flask_appbuilder import BaseView, expose
from app.extensions import db
from app.models.categoria import Categoria
from app.models.laptop import Laptop


class ReporteLaptopsView(BaseView):

    @expose("/", methods=["GET"])
    def list(self):
        categorias = db.session.query(Categoria).all()
        cat_id_sel = request.args.get("cat_id", "")

        # datos para la grfica de barras cantidad por categtia
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
