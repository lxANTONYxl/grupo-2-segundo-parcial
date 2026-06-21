from flask import Flask

from .extensions import appbuilder, db


def create_app() -> Flask:
    app = Flask(__name__)
    app.config.from_object("config")
    
    db.init_app(app)
    
    with app.app_context():
        appbuilder.init_app(app, db.session)
        
        from app.models.categoria import Categoria
        from app.models.marca import Marca
        from app.models.laptop import Laptop
        from app.models.cliente import Cliente
        from app.models.pedido import Pedido
        from app.models.detalle_pedido import DetallePedido
        
        db.create_all()
    return app
