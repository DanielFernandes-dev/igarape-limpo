import math

from flask import Blueprint, current_app, jsonify, request, session, url_for

import config
from app.integrations import nominatim, openmeteo, overpass, sensor_gateway
from app.repositories import ocorrencia_repository, ponto_repository
from app.services import (
    auth_service,
    estatistica_service,
    integracao_service,
    ocorrencia_service,
    ponto_service,
    limpeza_service,
)
from app.services.ocorrencia_service import ErroValidacao
from app.utils import http

api = Blueprint("api", __name__, url_prefix="/api")


def _usuario_atual():
    from flask import g

    return getattr(g, "current_user", None)


def _requer_autenticacao():
    usuario = _usuario_atual()
    if usuario is None:
        return jsonify({"erro": "Não autenticado."}), 401
    return usuario


# ------------------ Autenticação ------------------


@api.post("/auth/login")
def login():
    dados = request.get_json(silent=True) or {}
    if not isinstance(dados, dict):
        return jsonify({"erro": "Corpo JSON inválido."}), 400
    email = (dados.get("email") or "").strip().lower()
    senha = dados.get("senha") or ""
    if not email or not senha:
        return jsonify({"erro": "E-mail e senha são obrigatórios."}), 400
    try:
        usuario = auth_service.autenticar(email, senha)
    except auth_service.ErroValidacao as e:
        current_app.logger.warning("Falha de login de %s", request.remote_addr)
        return jsonify({"erro": e.mensagem}), e.status
    session["usuario_id"] = usuario["id"]
    current_app.logger.info("Login efetuado pelo usuário %s", usuario["id"])
    return jsonify({"usuario": auth_service.serializar(usuario)})


@api.post("/auth/cadastro")
def cadastro():
    dados = request.get_json(silent=True) or {}
    if not isinstance(dados, dict):
        return jsonify({"erro": "Corpo JSON inválido."}), 400
    dados_publicos = {
        "nome": dados.get("nome"),
        "email": dados.get("email"),
        "senha": dados.get("senha"),
        "perfil": "usuario",
    }
    try:
        novo_id = auth_service.criar_usuario(dados_publicos)
    except auth_service.ErroValidacao as e:
        return jsonify({"erro": e.mensagem}), e.status
    current_app.logger.info("Novo cadastro de usuário %s", novo_id)
    return jsonify({"id": novo_id}), 201


@api.post("/auth/logout")
def logout():
    usuario_id = session.get("usuario_id")
    session.pop("usuario_id", None)
    if usuario_id:
        current_app.logger.info("Logout efetuado pelo usuário %s", usuario_id)
    return jsonify({"ok": True})


@api.get("/auth/me")
def eu():
    usuario = _usuario_atual()
    if usuario is None:
        return jsonify({"erro": "Não autenticado."}), 401
    return jsonify({"usuario": auth_service.serializar(usuario)})


@api.get("/auth/usuarios")
def listar_usuarios():
    usuario = _requer_autenticacao()
    if isinstance(usuario, tuple):
        return usuario
    if usuario.get("perfil") not in ("moderador", "administrador"):
        return jsonify({"erro": "Sem permissão."}), 403
    itens = [auth_service.serializar(u) for u in auth_service.usuario_repository.listar_todos()]
    return jsonify({"usuarios": itens})


@api.post("/auth/usuarios")
def criar_usuario():
    usuario = _requer_autenticacao()
    if isinstance(usuario, tuple):
        return usuario
    if usuario.get("perfil") != "administrador":
        return jsonify({"erro": "Sem permissão."}), 403
    dados = request.get_json(silent=True) or {}
    if not isinstance(dados, dict):
        return jsonify({"erro": "Corpo JSON inválido."}), 400
    try:
        novo_id = auth_service.criar_usuario(dados)
    except auth_service.ErroValidacao as e:
        return jsonify({"erro": e.mensagem}), e.status
    current_app.logger.info("Usuário %s criado pelo administrador %s", novo_id, usuario["id"])
    return jsonify({"id": novo_id}), 201


# ------------------ Ocorrências ------------------


@api.get("/ocorrencias")
def listar_ocorrencias():
    try:
        filtros = ocorrencia_service.validar_filtros(request.args)
    except ErroValidacao as e:
        return jsonify({"erro": e.mensagem}), e.status
    return jsonify(ocorrencia_service.listar(filtros))


@api.get("/ocorrencias/<int:ocorrencia_id>")
def obter_ocorrencia(ocorrencia_id):
    r = ocorrencia_repository.obter_por_id(ocorrencia_id)
    if r is None:
        return jsonify({"erro": "Ocorrência não encontrada"}), 404
    return jsonify(ocorrencia_service.serializar(r))


@api.get("/denuncias/<string:protocolo>")
def acompanhar_denuncia(protocolo):
    r = ocorrencia_repository.obter_por_protocolo(protocolo)
    if r is None:
        return jsonify({"erro": "Denúncia não encontrada"}), 404
    item = {
        "protocolo": r["protocolo"],
        "data_hora": r["data_hora"],
        "ponto_nome": ocorrencia_service._nome_ponto(r["ponto_id"], None),
        "local_nome": r["local_nome"],
        "observacoes": r["observacoes"],
        "status": r["status"],
        "fotografia": (url_for("static", filename="uploads/" + r["fotografia"]) if r["fotografia"] else None),
    }
    return jsonify({"denuncia": item})


@api.post("/ocorrencias")
def criar_ocorrencia():
    usuario = _requer_autenticacao()
    if isinstance(usuario, tuple):
        return usuario
    formulario = request.form
    arquivo = request.files.get("fotografia")
    try:
        novo_id = ocorrencia_service.criar(formulario, arquivo)
    except ErroValidacao as e:
        return jsonify({"erro": e.mensagem}), e.status
    current_app.logger.info("Ocorrência %s criada pelo usuário %s", novo_id, usuario["id"])
    return (
        jsonify({
            "id": novo_id,
            "protocolo": ocorrencia_repository.obter_por_id(novo_id)["protocolo"],
            "url": url_for("pages.detalhe", ocorrencia_id=novo_id),
        }),
        201,
    )


@api.put("/ocorrencias/<int:ocorrencia_id>")
@api.patch("/ocorrencias/<int:ocorrencia_id>")
def atualizar_ocorrencia(ocorrencia_id):
    usuario = _requer_autenticacao()
    if isinstance(usuario, tuple):
        return usuario
    registro = ocorrencia_repository.obter_por_id(ocorrencia_id)
    if registro is None:
        return jsonify({"erro": "Ocorrência não encontrada"}), 404
    perfil_elevado = usuario.get("perfil") in ("moderador", "administrador")
    if not perfil_elevado and registro["usuario_id"] != usuario["id"]:
        return jsonify({"erro": "Sem permissão."}), 403
    if request.content_type and "application/json" in request.content_type:
        dados = request.get_json(silent=True) or {}
        arquivo = None
    else:
        dados = dict(request.form)
        arquivo = request.files.get("fotografia")
    if not isinstance(dados, dict):
        return jsonify({"erro": "Corpo JSON inválido."}), 400
    if "status" in dados and not perfil_elevado and dados["status"] != registro["status"]:
        return jsonify({"erro": "Sem permissão para alterar o status."}), 403
    try:
        ocorrencia_service.atualizar(ocorrencia_id, dados, arquivo)
    except ErroValidacao as e:
        return jsonify({"erro": e.mensagem}), e.status
    current_app.logger.info("Ocorrência %s atualizada pelo usuário %s", ocorrencia_id, usuario["id"])
    return jsonify({"id": ocorrencia_id})


@api.delete("/ocorrencias/<int:ocorrencia_id>")
def excluir_ocorrencia(ocorrencia_id):
    usuario = _requer_autenticacao()
    if isinstance(usuario, tuple):
        return usuario
    if usuario.get("perfil") not in ("moderador", "administrador"):
        return jsonify({"erro": "Sem permissão."}), 403
    try:
        ocorrencia_service.excluir(ocorrencia_id)
    except ErroValidacao as e:
        return jsonify({"erro": e.mensagem}), e.status
    current_app.logger.info("Ocorrência %s excluída pelo usuário %s", ocorrencia_id, usuario["id"])
    return jsonify({"id": ocorrencia_id, "excluida": True})


@api.errorhandler(413)
def arquivo_grande(e):
    return jsonify({"erro": "Arquivo muito grande. Máximo 10 MB."}), 413


# ------------------ Pontos monitorados ------------------


@api.get("/pontos")
def listar_pontos():
    pontos = ponto_service.listar_pontos()
    nivel = (request.args.get("acessibilidade") or "").strip()
    if nivel:
        if nivel not in config.NIVEIS_ACESSIBILIDADE:
            return jsonify({"erro": "Filtro de acessibilidade inválido."}), 400
        pontos = [p for p in pontos if p.get("nivel_acessibilidade") == nivel]
    return jsonify(pontos)


@api.get("/pontos/<int:ponto_id>")
def obter_ponto(ponto_id):
    resumo = ponto_service.obter_resumo_por_id(ponto_id)
    if resumo is None:
        return jsonify({"erro": "Ponto monitorado não encontrado"}), 404
    return jsonify(resumo)


@api.post("/pontos")
def criar_ponto():
    usuario = _requer_autenticacao()
    if isinstance(usuario, tuple):
        return usuario
    if usuario.get("perfil") not in ("moderador", "administrador"):
        return jsonify({"erro": "Sem permissão."}), 403
    try:
        novo_id = ponto_service.criar(request.form)
    except ErroValidacao as e:
        return jsonify({"erro": e.mensagem}), e.status
    return jsonify({"id": novo_id, "url": url_for("pages.ponto", ponto_id=novo_id)}), 201


@api.patch("/pontos/<int:ponto_id>")
@api.put("/pontos/<int:ponto_id>")
def atualizar_ponto(ponto_id):
    usuario = _requer_autenticacao()
    if isinstance(usuario, tuple):
        return usuario
    if usuario.get("perfil") not in ("moderador", "administrador"):
        return jsonify({"erro": "Sem permissão."}), 403
    dados = request.get_json(silent=True) if request.is_json else dict(request.form)
    if not isinstance(dados, dict):
        return jsonify({"erro": "Corpo JSON inválido."}), 400
    try:
        ponto_service.atualizar(ponto_id, dados)
    except ponto_service.PontoNaoEncontrado:
        return jsonify({"erro": "Ponto monitorado não encontrado"}), 404
    except ErroValidacao as e:
        return jsonify({"erro": e.mensagem}), e.status
    return jsonify({"id": ponto_id})


@api.get("/pontos/<int:ponto_id>/historico")
def historico_ponto(ponto_id):
    resumo = ponto_service.obter_resumo_por_id(ponto_id)
    if resumo is None:
        return jsonify({"erro": "Ponto monitorado não encontrado"}), 404
    return jsonify({"ocorrencias": resumo["ocorrencias"]})


@api.get("/pontos/<int:ponto_id>/limpezas")
def listar_limpezas(ponto_id):
    if ponto_repository.obter_por_id(ponto_id) is None:
        return jsonify({"erro": "Ponto monitorado não encontrado"}), 404
    return jsonify({"limpezas": limpeza_service.listar_por_ponto(ponto_id)})


@api.post("/pontos/<int:ponto_id>/limpezas")
def criar_limpeza(ponto_id):
    usuario = _requer_autenticacao()
    if isinstance(usuario, tuple):
        return usuario
    if usuario.get("perfil") not in ("moderador", "administrador"):
        return jsonify({"erro": "Sem permissão."}), 403
    dados = dict(request.form)
    dados["ponto_id"] = ponto_id
    try:
        novo_id = limpeza_service.criar(dados, request.files.get("fotografia"))
    except ErroValidacao as e:
        return jsonify({"erro": e.mensagem}), e.status
    current_app.logger.info("Limpeza %s registrada pelo usuário %s", novo_id, usuario["id"])
    return jsonify({"id": novo_id}), 201


# ------------------ Dashboard ------------------


@api.get("/dashboard/resumo")
def dashboard_resumo():
    return jsonify(estatistica_service.resumo())


@api.get("/dashboard/series")
def dashboard_series():
    try:
        periodo = int(request.args.get("dias", 30))
    except (TypeError, ValueError):
        periodo = 30
    if not 1 <= periodo <= 365:
        periodo = 30
    return jsonify(estatistica_service.series(periodo))


@api.get("/dashboard/ranking")
def dashboard_ranking():
    try:
        limite = int(request.args.get("limite", 10))
    except (TypeError, ValueError):
        limite = 10
    return jsonify({"ranking": estatistica_service.ranking(min(limite, 50))})


@api.get("/dashboard/comparacao")
def dashboard_comparacao():
    try:
        dias = int(request.args.get("dias", 7))
    except (TypeError, ValueError):
        dias = 7
    if not 1 <= dias <= 90:
        dias = 7
    return jsonify(estatistica_service.comparacao_periodos(dias))


# ------------------ Exportação ------------------


@api.get("/export/ocorrencias.csv")
def exportar_ocorrencias():
    try:
        filtros = ocorrencia_service.validar_filtros(request.args)
    except ocorrencia_service.ErroValidacao as e:
        return jsonify({"erro": e.mensagem}), e.status
    csv = ocorrencia_service.exportar_csv_ocorrencias(filtros)
    nome = "ocorrencias.csv"
    return _responder_csv(csv, nome)


@api.get("/export/ocorrencias.geojson")
def exportar_ocorrencias_geojson():
    try:
        filtros = ocorrencia_service.validar_filtros(request.args)
    except ocorrencia_service.ErroValidacao as e:
        return jsonify({"erro": e.mensagem}), e.status
    return jsonify(ocorrencia_service.exportar_geojson_ocorrencias(filtros))


# ------------------ Integrações ------------------


@api.get("/integracao/hidrografia")
def hidrografia():
    try:
        resultado = overpass.buscar_hidrografia(
            config.BOUNDING_BOX,
            trechos_maximo=config.MAX_HIDROGRAFIA_TRECHOS,
        )
        return jsonify(resultado)
    except http.HttpError as e:
        return jsonify({"erro": e.message}), 502


@api.get("/integracao/meteo")
def meteo():
    lat = request.args.get("lat")
    lon = request.args.get("lon")
    if lat is None or lon is None:
        return jsonify({"erro": "Parâmetros lat e lon são obrigatórios."}), 400
    try:
        latitude, longitude = _coordenadas_integracao(lat, lon)
        resultado = openmeteo.buscar_clima(latitude, longitude)
        return jsonify(resultado)
    except (ValueError, OverflowError):
        return jsonify({"erro": "Coordenadas inválidas."}), 400
    except http.HttpError as e:
        return jsonify({"erro": e.message}), 502


@api.get("/integracao/geocode")
def geocode():
    lat = request.args.get("lat")
    lon = request.args.get("lon")
    if lat is None or lon is None:
        return jsonify({"erro": "Parâmetros lat e lon são obrigatórios."}), 400
    try:
        latitude, longitude = _coordenadas_integracao(lat, lon)
        resultado = nominatim.buscar_local(latitude, longitude)
        return jsonify(resultado)
    except (ValueError, OverflowError):
        return jsonify({"erro": "Coordenadas inválidas."}), 400
    except http.HttpError as e:
        return jsonify({"erro": e.message}), 502


@api.post("/integracao/sensores")
def sensores():
    corpo = request.get_json(silent=True) or {}
    if not isinstance(corpo, dict):
        return jsonify({"erro": "Corpo JSON inválido."}), 400
    url = (corpo.get("url") or "").strip()
    token = (corpo.get("token") or "").strip() or None
    if not url:
        return jsonify({"erro": "Informe a URL do gateway."}), 400
    try:
        estacoes = sensor_gateway.conectar_gateway(url, token)
        return jsonify({"estacoes": estacoes})
    except http.HttpError as e:
        return jsonify({"erro": e.message}), 502


@api.get("/integracao/status")
def status_integracoes():
    return jsonify(integracao_service.status_integracoes())


@api.post("/export/sensores.csv")
def exportar_sensores():
    corpo = request.get_json(silent=True) or {}
    if not isinstance(corpo, dict):
        return jsonify({"erro": "Corpo JSON inválido."}), 400
    url = (corpo.get("url") or "").strip()
    token = (corpo.get("token") or "").strip() or None
    if not url:
        return jsonify({"erro": "Informe a URL do gateway."}), 400
    try:
        csv = ocorrencia_service.exportar_csv_sensores(url, token)
    except http.HttpError as e:
        return jsonify({"erro": e.message}), 502
    return _responder_csv(csv, "sensores.csv")


def _responder_csv(conteudo, nome_arquivo):
    from flask import Response

    return Response(
        conteudo,
        mimetype="text/csv",
        headers={"Content-Disposition": f"attachment; filename={nome_arquivo}"},
    )


def _coordenadas_integracao(latitude, longitude):
    latitude = float(latitude)
    longitude = float(longitude)
    if not math.isfinite(latitude) or not math.isfinite(longitude):
        raise ValueError
    if not (-90 <= latitude <= 90 and -180 <= longitude <= 180):
        raise ValueError
    return latitude, longitude
