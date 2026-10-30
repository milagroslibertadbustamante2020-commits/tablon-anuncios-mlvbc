# Autor: Milagros L. V. Bustamante Chuquimia (MLVBC) - TEM-742
from flask import Flask
from config import Config
from app.extensions import db


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)

    # Registro de los blueprints (modulos)
    from app.auth.routes import auth_bp
    from app.main.routes import main_bp
    from app.usuarios.routes import usuarios_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(main_bp)
    app.register_blueprint(usuarios_bp)

    # Crea las tablas de bd_anuncios y el usuario inicial
    with app.app_context():
        from app import models
        db.create_all()
        models.crear_datos_iniciales()

    return app
