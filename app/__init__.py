import os

from flask import Flask, g, session

import database
import config
from config import COR_NIVEIS, MAX_CONTENT_LENGTH, NIVEIS_ACUMULO, SECRET_KEY, STATUS_OCORRENCIA, TIPOS_RESIDUO, UPLOAD_FOLDER


def create_app():
    template_dir = os.path.join(config.BASE_DIR, "templates")
    static_dir = os.path.join(config.BASE_DIR, "static")
    app = Flask(__name__, template_folder=template_dir, static_folder=static_dir)
    app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
    app.config["MAX_CONTENT_LENGTH"] = MAX_CONTENT_LENGTH
    app.config["SECRET_KEY"] = SECRET_KEY

    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    database.init_app(app)

    @app.before_request
    def carregar_usuario():
        usuario_id = session.get("usuario_id")
        g.current_user = None
        if usuario_id:
            from app.services import auth_service
            g.current_user = auth_service.obter_por_id(usuario_id)

    @app.context_processor
    def inject_constants():
        return {
            "tipos_residuo": TIPOS_RESIDUO,
            "niveis_acumulo": NIVEIS_ACUMULO,
            "cor_niveis": COR_NIVEIS,
            "status_ocorrencia": STATUS_OCORRENCIA,
            "current_user": getattr(g, "current_user", None),
        }

    from app.routes import registrar_blueprints

    registrar_blueprints(app)

    return app
