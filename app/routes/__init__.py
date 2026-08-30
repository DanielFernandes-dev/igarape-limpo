from flask import Blueprint

from app.routes.api import api
from app.routes.pages import pages


def registrar_blueprints(app):
    app.register_blueprint(pages)
    app.register_blueprint(api)
