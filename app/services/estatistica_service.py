from datetime import datetime, timedelta

import database
from app.repositories import ocorrencia_repository, ponto_repository
from app.services.ponto_service import LIMIAR_RECORRENCIA


def resumo():
    ocorrencias = [dict(o) for o in ocorrencia_repository.listar_todas()]
    pontos = [dict(p) for p in ponto_repository.listar_todos()]

    agora = datetime.now()
    sete = agora - timedelta(days=7)
    trinta = agora - timedelta(days=30)

    total = len(ocorrencias)
    ultimos_7 = _contar_apos(ocorrencias, sete)
    ultimos_30 = _contar_apos(ocorrencias, trinta)

    pontos_ativos = sum(1 for p in pontos if p.get("status") == "Ativo")

    por_tipo = _contar(ocorrencias, "tipo_residuo")
    por_nivel = _contar(ocorrencias, "nivel_acumulo")

    residuo_frequente = _mais_frequente(por_tipo)
    nivel_frequente = _mais_frequente(por_nivel)

    local_maior = None
    por_local = _contar(ocorrencias, "local_nome")
    if por_local:
        local_maior = {
            "nome": _mais_frequente(por_local),
            "quantidade": por_local[_mais_frequente(por_local)],
        }

    pontos_criticos = sum(
        1 for p in pontos if (p.get("total_ocorrencias") or 0) >= LIMIAR_RECORRENCIA
    )
    ocorrencias_recorrentes = _contar_recorrentes(pontos)

    return {
        "total_ocorrencias": total,
        "ultimos_7_dias": ultimos_7,
        "ultimos_30_dias": ultimos_30,
        "pontos_monitorados": len(pontos),
        "pontos_ativos": pontos_ativos,
        "pontos_criticos": pontos_criticos,
        "ocorrencias_recorrentes": ocorrencias_recorrentes,
        "residuo_mais_frequente": residuo_frequente,
        "nivel_mais_frequente": nivel_frequente,
        "local_maior_ocorrencia": local_maior,
        "por_tipo": por_tipo,
        "por_nivel": por_nivel,
    }


def series(periodo_dias=30):
    ocorrencias = [dict(o) for o in ocorrencia_repository.listar_todas()]
    hoje = datetime.now().date()
    inicio = hoje - timedelta(days=periodo_dias - 1)

    dias = {}
    for i in range(periodo_dias):
        dia = inicio + timedelta(days=i)
        dias[dia.isoformat()] = 0

    chave_formats = []
    for o in ocorrencias:
        try:
            data = datetime.fromisoformat(o["data_hora"]).date()
        except (TypeError, ValueError):
            continue
        if inicio <= data <= hoje:
            chave = data.isoformat()
            if chave in dias:
                dias[chave] += 1

    return {
        "periodo_dias": periodo_dias,
        "inicio": inicio.isoformat(),
        "fim": hoje.isoformat(),
        "pontos": [{"data": k, "quantidade": v} for k, v in sorted(dias.items())],
    }


def ranking(limite=10):
    pontos = [dict(p) for p in ponto_repository.listar_todos()]
    ordenados = sorted(
        pontos, key=lambda p: p.get("total_ocorrencias") or 0, reverse=True
    )
    ranking = [
        {
            "id": p["id"],
            "nome": p["nome"],
            "quantidade": p.get("total_ocorrencias") or 0,
            "status": p.get("status"),
        }
        for p in ordenados[:limite]
    ]
    return ranking


def _contar_apos(ocorrencias, momento):
    contagem = 0
    for o in ocorrencias:
        try:
            data = datetime.fromisoformat(o["data_hora"])
        except (TypeError, ValueError):
            continue
        if data >= momento:
            contagem += 1
    return contagem


def _contar(ocorrencias, campo):
    resultado = {}
    for o in ocorrencias:
        valor = o.get(campo)
        if valor:
            resultado[valor] = resultado.get(valor, 0) + 1
    return resultado


def _mais_frequente(contagem):
    if not contagem:
        return None
    return max(contagem, key=contagem.get)


def _contar_recorrentes(pontos):
    return sum(
        1 for p in pontos if (p.get("total_ocorrencias") or 0) >= LIMIAR_RECORRENCIA
    )
