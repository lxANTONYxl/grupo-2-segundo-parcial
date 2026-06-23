from flask_appbuilder import BaseView, expose
from app.extensions import db


class ReporteTopView(BaseView):
    """
    Reporte 3 (Integrante 3 - Antony):
    Muestra el ranking de laptops más vendidas (por cantidad)
    y una gráfica de línea con los ingresos totales por mes.
    """

    @expose("/", methods=["GET"])
    def list(self):
        return self.render_template("reportes/reporte_top.html")