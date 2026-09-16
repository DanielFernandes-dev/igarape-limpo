from flask import Blueprint, abort, g, redirect, render_template

from app.repositories import ocorrencia_repository, ponto_repository
from app.services import ponto_service

pages = Blueprint("pages", __name__)


@pages.get("/")
def index():
    pontos = ponto_service.listar_pontos()
    return render_template("index.html", pontos=pontos)


@pages.get("/nova")
def nova():
    pontos = ponto_service.listar_pontos()
    return render_template("nova_ocorrencia.html", pontos=pontos)


@pages.get("/ocorrencia/<int:ocorrencia_id>")
def detalhe(ocorrencia_id):
    o = ocorrencia_repository.obter_por_id(ocorrencia_id)
    if o is None:
        return render_template("nao_encontrado.html"), 404
    return render_template("ocorrencia.html", o=o)


@pages.get("/ponto/<int:ponto_id>")
def ponto(ponto_id):
    resumo = ponto_service.obter_resumo_por_id(ponto_id)
    if resumo is None:
        return render_template("nao_encontrado.html"), 404
    return render_template("ponto.html", p=resumo)


@pages.get("/dashboard")
def dashboard():
    return render_template("dashboard.html")


@pages.get("/operador")
def operador():
    usuario = getattr(g, "current_user", None)
    if usuario is None:
        return redirect("/login")
    if usuario.get("perfil") not in ("moderador", "administrador"):
        abort(403)
    return render_template("operador.html")


@pages.get("/login")
def login():
    from flask import session

    if session.get("usuario_id"):
        return redirect("/")
    return render_template("login.html")


@pages.get("/cadastro")
def cadastro():
    if getattr(g, "current_user", None):
        return redirect("/")
    return render_template("cadastro.html")


@pages.post("/logout")
def logout():
    from flask import session

    session.pop("usuario_id", None)
    return redirect("/")

