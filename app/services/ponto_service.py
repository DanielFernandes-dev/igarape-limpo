from app.repositories import ocorrencia_repository, ponto_repository
from app.services.ocorrencia_service import ErroValidacao

LIMIAR_RECORRENCIA = 3
JANELA_RECORRENCIA_DIAS = 90


class PontoNaoEncontrado(Exception):
    pass


def validar_dados(dados):
    nome = (dados.get("nome") or "").strip()
    if not nome:
        raise ErroValidacao("O nome do ponto é obrigatório.")
    if len(nome) > 120:
        raise ErroValidacao("O nome do ponto excede 120 caracteres.")

    try:
        latitude = float(dados.get("latitude"))
        longitude = float(dados.get("longitude"))
    except (TypeError, ValueError):
        raise ErroValidacao("Coordenadas inválidas.")

    if not (-90.0 <= latitude <= 90.0) or not (-180.0 <= longitude <= 180.0):
        raise ErroValidacao("Coordenadas fora do intervalo válido.")

    status = (dados.get("status") or "Ativo").strip()
    if status not in ("Ativo", "Inativo"):
        raise ErroValidacao("Status do ponto inválido.")

    descricao = (dados.get("descricao") or "").strip()
    if len(descricao) > 1000:
        raise ErroValidacao("A descrição excede 1000 caracteres.")

    return {
        "nome": nome,
        "latitude": latitude,
        "longitude": longitude,
        "descricao": descricao or None,
        "status": status,
    }


def criar(dados_form):
    dados = validar_dados(dados_form)
    return ponto_repository.criar(dados)


def atualizar(ponto_id, dados_form):
    registro = ponto_repository.obter_por_id(ponto_id)
    if registro is None:
        raise PontoNaoEncontrado()
    dados = validar_dados(dados_form)
    ponto_repository.atualizar(ponto_id, dados)
    return ponto_id


def obter_resumo_por_id(ponto_id):
    ponto = ponto_repository.obter_por_id(ponto_id)
    if ponto is None:
        return None

    ocorrencias = [dict(o) for o in ponto_repository.historico(ponto_id, limite=500)]
    return montar_resumo_ponto(dict(ponto), ocorrencias)


def montar_resumo_ponto(ponto, ocorrencias):
    from datetime import datetime, timedelta

    limite = datetime.utcnow() - timedelta(days=JANELA_RECORRENCIA_DIAS)
    ocorrencias_recorrencia = []
    for ocorrencia in ocorrencias:
        try:
            data = datetime.fromisoformat(ocorrencia["data_hora"])
        except (KeyError, TypeError, ValueError):
            continue
        if data >= limite:
            ocorrencias_recorrencia.append(ocorrencia)
    total = len(ocorrencias)
    por_tipo = _contar(ocorrencias, "tipo_residuo")
    por_nivel = _contar(ocorrencias, "nivel_acumulo")
    por_status = _contar(ocorrencias, "status")

    ultima = ocorrencias[0] if ocorrencias else None
    recorrente = len(ocorrencias_recorrencia) >= LIMIAR_RECORRENCIA
    foto_recente = next(
        (o for o in ocorrencias if o.get("fotografia")), None
    )

    return {
        "id": ponto["id"],
        "nome": ponto["nome"],
        "latitude": ponto["latitude"],
        "longitude": ponto["longitude"],
        "descricao": ponto.get("descricao"),
        "status": ponto.get("status"),
        "total_ocorrencias": total,
        "recorrente": recorrente,
        "limiar_recorrencia": LIMIAR_RECORRENCIA,
        "ultima_ocorrencia": _data_hora(ultima),
        "ultimo_nivel": ultima["nivel_acumulo"] if ultima else None,
        "por_tipo": por_tipo,
        "por_nivel": por_nivel,
        "por_status": por_status,
        "fotografia_recente": _url_foto(foto_recente),
        "ocorrencias": [_resumo_ocorrencia(o) for o in ocorrencias],
        "janela_recorrencia_dias": JANELA_RECORRENCIA_DIAS,
    }


def listar_pontos():
    pontos = [dict(p) for p in ponto_repository.listar_todos()]
    for p in pontos:
        p["recorrente"] = (p.get("ocorrencias_recentes") or 0) >= LIMIAR_RECORRENCIA
    return pontos


def _contar(ocorrencias, campo):
    resultado = {}
    for o in ocorrencias:
        valor = o.get(campo)
        if valor:
            resultado[valor] = resultado.get(valor, 0) + 1
    return resultado


def _data_hora(ocorrencia):
    return ocorrencia["data_hora"] if ocorrencia else None


def _resumo_ocorrencia(o):
    return {
        "id": o["id"],
        "data_hora": o["data_hora"],
        "tipo_residuo": o["tipo_residuo"],
        "nivel_acumulo": o["nivel_acumulo"],
        "status": o["status"],
        "fotografia": _url_foto(o),
    }


def _url_foto(o):
    if not o or not o.get("fotografia"):
        return None
    from flask import url_for

    return url_for("static", filename="uploads/" + o["fotografia"])
