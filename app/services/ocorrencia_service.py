import os
import uuid

from flask import g, url_for

import config
from app.integrations import sensor_gateway
from app.repositories import ocorrencia_repository, ponto_repository


def _usuario_autenticado():
    usuario = getattr(g, "current_user", None)
    if usuario:
        return usuario["id"]
    return None


class ErroValidacao(Exception):
    def __init__(self, mensagem, status=400):
        super().__init__(mensagem)
        self.mensagem = mensagem
        self.status = status


def validar_dados(dados):
    try:
        latitude = float(dados.get("latitude"))
        longitude = float(dados.get("longitude"))
    except (TypeError, ValueError):
        raise ErroValidacao("Coordenadas inválidas.")

    if not (-90.0 <= latitude <= 90.0) or not (-180.0 <= longitude <= 180.0):
        raise ErroValidacao("Coordenadas fora do intervalo válido.")

    tipo = dados.get("tipo_residuo", "").strip()
    nivel = dados.get("nivel_acumulo", "").strip()
    if tipo not in config.TIPOS_RESIDUO:
        raise ErroValidacao("Tipo de resíduo inválido.")
    if nivel not in config.NIVEIS_ACUMULO:
        raise ErroValidacao("Nível de acúmulo inválido.")

    status = (dados.get("status") or "Nova").strip()
    if status not in config.STATUS_OCORRENCIA:
        raise ErroValidacao("Status da ocorrência inválido.")

    ponto_id = None
    if dados.get("ponto_id") not in (None, ""):
        ponto_id = _validar_ponto_id(dados.get("ponto_id"))

    return {
        "ponto_id": ponto_id,
        "latitude": latitude,
        "longitude": longitude,
        "tipo_residuo": tipo,
        "nivel_acumulo": nivel,
        "status": status,
        "observacoes": dados.get("observacoes", "").strip() or None,
        "local_nome": dados.get("local_nome", "").strip() or None,
        "fotografia": None,
    }


def _validar_ponto_id(valor):
    try:
        ponto_id = int(valor)
    except (TypeError, ValueError):
        raise ErroValidacao("Ponto monitorado inválido.")
    if ponto_repository.obter_por_id(ponto_id) is None:
        raise ErroValidacao("Ponto monitorado não encontrado.")
    return ponto_id


def validar_filtros(args):
    """Valida e normaliza os parâmetros de filtro da listagem."""
    filtros = {}

    tipo = (args.get("tipo_residuo") or "").strip()
    if tipo:
        if tipo not in config.TIPOS_RESIDUO:
            raise ErroValidacao("Filtro de tipo de resíduo inválido.")
        filtros["tipo_residuo"] = tipo

    nivel = (args.get("nivel_acumulo") or "").strip()
    if nivel:
        if nivel not in config.NIVEIS_ACUMULO:
            raise ErroValidacao("Filtro de nível de acúmulo inválido.")
        filtros["nivel_acumulo"] = nivel

    ponto_id = (args.get("ponto_id") or "").strip()
    if ponto_id:
        filtros["ponto_id"] = _validar_ponto_id(ponto_id)

    busca = (args.get("busca") or "").strip()
    if busca:
        filtros["busca"] = busca

    data_inicio = (args.get("data_inicio") or "").strip()
    if data_inicio:
        _validar_data(data_inicio)
        filtros["data_inicio"] = data_inicio

    data_fim = (args.get("data_fim") or "").strip()
    if data_fim:
        _validar_data(data_fim)
        filtros["data_fim"] = data_fim

    return filtros


def _validar_data(valor):
    from datetime import date

    try:
        date.fromisoformat(valor)
    except ValueError:
        raise ErroValidacao("Formato de data inválido. Use AAAA-MM-DD.")



def salvar_fotografia(arquivo):
    if arquivo is None or not arquivo.filename:
        return None
    if not _extensao_permitida(arquivo.filename):
        raise ErroValidacao("Formato de imagem não permitido.")
    extensao = arquivo.filename.rsplit(".", 1)[-1].lower()
    nome = f"ocorr_{uuid.uuid4().hex}.{extensao}"
    arquivo.save(os.path.join(config.UPLOAD_FOLDER, nome))
    return nome


def criar(dados_form, arquivo_foto=None):
    dados = validar_dados(dados_form)
    dados["fotografia"] = salvar_fotografia(arquivo_foto)
    dados["usuario_id"] = _usuario_autenticado()
    novo_id = ocorrencia_repository.criar(dados)
    return novo_id


def atualizar(ocorrencia_id, dados_form, arquivo_foto=None):
    registro = ocorrencia_repository.obter_por_id(ocorrencia_id)
    if registro is None:
        raise ErroValidacao("Ocorrência não encontrada.", status=404)

    dados_mesclados = dict(registro)
    dados_mesclados.update({k: v for k, v in dados_form.items() if v is not None and v != ""})
    if "ponto_id" in dados_mesclados and dados_mesclados["ponto_id"] in (None, ""):
        dados_mesclados["ponto_id"] = None

    dados = validar_dados(dados_mesclados)
    dados["fotografia"] = _fotografia_atualizada(registro, arquivo_foto)
    dados["usuario_id"] = _usuario_autenticado()
    linha = ocorrencia_repository.atualizar(ocorrencia_id, dados)
    if linha == 0:
        raise ErroValidacao("Ocorrência não encontrada.", status=404)
    return ocorrencia_id


def excluir(ocorrencia_id):
    registro = ocorrencia_repository.obter_por_id(ocorrencia_id)
    if registro is None:
        raise ErroValidacao("Ocorrência não encontrada.", status=404)
    _remover_arquivo(registro["fotografia"])
    ocorrencia_repository.excluir(ocorrencia_id)
    return ocorrencia_id


def _fotografia_atualizada(registro, arquivo_foto):
    novo_nome = salvar_fotografia(arquivo_foto)
    if novo_nome:
        _remover_arquivo(registro["fotografia"])
        return novo_nome
    return registro["fotografia"]


def _remover_arquivo(nome):
    if not nome:
        return
    caminho = os.path.join(config.UPLOAD_FOLDER, nome)
    if os.path.exists(caminho):
        os.remove(caminho)


def serializar(registro, pontos_cache=None):
    item = dict(registro)
    item["fotografia"] = (
        url_for("static", filename="uploads/" + registro["fotografia"])
        if registro["fotografia"]
        else None
    )
    item["cor"] = config.COR_NIVEIS.get(registro["nivel_acumulo"], "#64748b")
    item["ponto_nome"] = _nome_ponto(registro["ponto_id"], pontos_cache)
    return item


def listar(filtros):
    registros = ocorrencia_repository.listar_todas(filtros)
    total = ocorrencia_repository.contar(filtros)
    pontos = {
        p["id"]: p["nome"] for p in ponto_repository.listar_todos()
    }
    itens = [serializar(r, pontos) for r in registros]
    return {"total": total, "ocorrencias": itens}


def _nome_ponto(ponto_id, pontos_cache):
    if ponto_id is None:
        return None
    if pontos_cache is None:
        ponto = ponto_repository.obter_por_id(ponto_id)
        return ponto["nome"] if ponto else None
    return pontos_cache.get(ponto_id)


def _extensao_permitida(nome_arquivo):
    return (
        "." in nome_arquivo
        and nome_arquivo.rsplit(".", 1)[1].lower() in config.ALLOWED_EXTENSIONS
    )


def exportar_csv_ocorrencias():
    from app.utils import export

    linhas = [dict(r) for r in ocorrencia_repository.listar_todas()]
    return export.to_csv(export.ocorrencias_para_linhas(linhas))


def exportar_geojson_ocorrencias():
    from app.utils import export

    linhas = [dict(r) for r in ocorrencia_repository.listar_todas()]
    return export.to_geojson(export.ocorrencias_para_geojson(linhas))


def exportar_csv_sensores(url, token=None):
    from app.utils import export

    estacoes = sensor_gateway.conectar_gateway(url, token)
    return export.to_csv(export.sensores_para_linhas(estacoes))
