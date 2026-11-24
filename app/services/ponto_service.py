import config
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

    nivel_acessibilidade = (dados.get("nivel_acessibilidade") or "").strip()
    if nivel_acessibilidade and nivel_acessibilidade not in config.NIVEIS_ACESSIBILIDADE:
        raise ErroValidacao("Nível de acessibilidade inválido.")
    observacoes_acesso = (dados.get("observacoes_acesso") or "").strip()
    if len(observacoes_acesso) > 1000:
        raise ErroValidacao("Observações de acesso excedem 1000 caracteres.")
    data_avaliacao = (dados.get("data_avaliacao_acesso") or "").strip()
    if nivel_acessibilidade and not data_avaliacao:
        from datetime import datetime
        data_avaliacao = datetime.now().isoformat(timespec="minutes")
    if data_avaliacao:
        from datetime import datetime
        try:
            datetime.fromisoformat(data_avaliacao)
        except ValueError:
            raise ErroValidacao("Data da avaliação de acessibilidade inválida.")

    from flask import g
    usuario = getattr(g, "current_user", None)
    responsavel_id = None
    if nivel_acessibilidade:
        responsavel_id = usuario["id"] if usuario else dados.get("responsavel_avaliacao_id")

    return {
        "nome": nome,
        "latitude": latitude,
        "longitude": longitude,
        "descricao": descricao or None,
        "status": status,
        "nivel_acessibilidade": nivel_acessibilidade or None,
        "observacoes_acesso": observacoes_acesso or None,
        "data_avaliacao_acesso": data_avaliacao or None,
        "responsavel_avaliacao_id": responsavel_id,
    }


def criar(dados_form):
    dados = validar_dados(dados_form)
    return ponto_repository.criar(dados)


def atualizar(ponto_id, dados_form):
    registro = ponto_repository.obter_por_id(ponto_id)
    if registro is None:
        raise PontoNaoEncontrado()
    dados_mesclados = dict(registro)
    dados_mesclados.update({k: v for k, v in dados_form.items() if v is not None})
    dados = validar_dados(dados_mesclados)
    ponto_repository.atualizar(ponto_id, dados)
    return ponto_id


def obter_resumo_por_id(ponto_id):
    ponto = ponto_repository.obter_por_id(ponto_id)
    if ponto is None:
        return None

    ocorrencias = [dict(o) for o in ponto_repository.historico(ponto_id, limite=500)]
    estatisticas = ponto_repository.estatisticas_ocorrencias(ponto_id)
    return montar_resumo_ponto(dict(ponto), ocorrencias, estatisticas)


def montar_resumo_ponto(ponto, ocorrencias, estatisticas=None):
    from datetime import datetime, timedelta
    from app.repositories import limpeza_repository

    limite = datetime.utcnow() - timedelta(days=JANELA_RECORRENCIA_DIAS)
    estatisticas = estatisticas or {}
    ocorrencias_recorrencia = []
    for ocorrencia in ocorrencias:
        try:
            data = datetime.fromisoformat(ocorrencia["data_hora"])
        except (KeyError, TypeError, ValueError):
            continue
        if data >= limite:
            ocorrencias_recorrencia.append(ocorrencia)
    total = estatisticas.get("total", len(ocorrencias))
    por_tipo = estatisticas.get("por_tipo", _contar(ocorrencias, "tipo_residuo"))
    por_nivel = estatisticas.get("por_nivel", _contar(ocorrencias, "nivel_acumulo"))
    por_status = estatisticas.get("por_status", _contar(ocorrencias, "status"))

    ultima = ocorrencias[0] if ocorrencias else None
    limpezas = limpeza_repository.listar_por_ponto(ponto["id"])
    ultima_limpeza = limpezas[0] if limpezas else None
    novas_apos_limpeza = 0
    if ultima_limpeza:
        from app.repositories import ocorrencia_repository
        novas_apos_limpeza = ocorrencia_repository.contar_apos_limpeza(
            ponto["id"], ultima_limpeza["data_hora"]
        )
    recorrente = estatisticas.get("recentes", len(ocorrencias_recorrencia)) >= LIMIAR_RECORRENCIA
    foto_recente = {"fotografia": estatisticas.get("fotografia_recente")} if estatisticas.get("fotografia_recente") else next(
        (o for o in ocorrencias if o.get("fotografia")), None
    )

    return {
        "id": ponto["id"],
        "nome": ponto["nome"],
        "latitude": ponto["latitude"],
        "longitude": ponto["longitude"],
        "descricao": ponto.get("descricao"),
        "status": ponto.get("status"),
        "nivel_acessibilidade": ponto.get("nivel_acessibilidade"),
        "observacoes_acesso": ponto.get("observacoes_acesso"),
        "data_avaliacao_acesso": ponto.get("data_avaliacao_acesso"),
        "responsavel_avaliacao_nome": ponto.get("responsavel_avaliacao_nome"),
        "total_ocorrencias": total,
        "total_limpezas": len(limpezas),
        "ultima_limpeza": ultima_limpeza["data_hora"] if ultima_limpeza else None,
        "novas_ocorrencias_apos_limpeza": novas_apos_limpeza,
        "houve_reincidencia": bool(ultima_limpeza and novas_apos_limpeza > 0),
        "limpezas": [
            {
                "id": dict(l)["id"], "data_hora": dict(l)["data_hora"], "equipe": dict(l).get("equipe"),
                "quantidade": dict(l).get("quantidade"), "unidade": dict(l).get("unidade"),
                "observacoes": dict(l).get("observacoes"), "fotografia": _url_limpeza(dict(l)),
            } for l in limpezas
        ],
        "recorrente": recorrente,
        "limiar_recorrencia": LIMIAR_RECORRENCIA,
        "ultima_ocorrencia": estatisticas.get("ultima_ocorrencia") or _data_hora(ultima),
        "ultimo_nivel": estatisticas.get("ultimo_nivel") or (ultima["nivel_acumulo"] if ultima else None),
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
        p.pop("responsavel_avaliacao_id", None)
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


def _url_limpeza(l):
    if not l or not l.get("fotografia"):
        return None
    from flask import url_for
    return url_for("static", filename="uploads/" + l["fotografia"])
