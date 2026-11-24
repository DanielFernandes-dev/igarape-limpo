import database


def listar_todos():
    return database.query_all(
        """
        SELECT p.*,
                             (SELECT COUNT(*) FROM ocorrencias o WHERE o.ponto_id = p.id) AS total_ocorrencias,
                             (SELECT COUNT(*) FROM ocorrencias o
                                WHERE o.ponto_id = p.id
                                    AND o.data_hora >= datetime('now', '-90 days')) AS ocorrencias_recentes,
               (SELECT nivel_acumulo FROM ocorrencias o
                WHERE o.ponto_id = p.id ORDER BY o.data_hora DESC LIMIT 1) AS ultimo_nivel
        FROM pontos_monitorados p
        ORDER BY p.nome
        """
    )


def obter_por_id(ponto_id):
    return database.query_one(
        """
        SELECT p.*, u.nome AS responsavel_avaliacao_nome
        FROM pontos_monitorados p
        LEFT JOIN usuarios u ON u.id = p.responsavel_avaliacao_id
        WHERE p.id = ?
        """,
        (ponto_id,),
    )


def criar(dados):
    return database.query_insert(
        """
        INSERT INTO pontos_monitorados
            (nome, latitude, longitude, descricao, status, nivel_acessibilidade,
             observacoes_acesso, data_avaliacao_acesso, responsavel_avaliacao_id)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            dados["nome"],
            dados["latitude"],
            dados["longitude"],
            dados.get("descricao"),
            dados.get("status", "Ativo"),
            dados.get("nivel_acessibilidade"),
            dados.get("observacoes_acesso"),
            dados.get("data_avaliacao_acesso"),
            dados.get("responsavel_avaliacao_id"),
        ),
    )


def atualizar(ponto_id, dados):
    return database.query_update(
        """
        UPDATE pontos_monitorados
        SET nome = ?, latitude = ?, longitude = ?, descricao = ?, status = ?,
            nivel_acessibilidade = ?, observacoes_acesso = ?,
            data_avaliacao_acesso = ?, responsavel_avaliacao_id = ?
        WHERE id = ?
        """,
        (
            dados["nome"],
            dados["latitude"],
            dados["longitude"],
            dados.get("descricao"),
            dados.get("status", "Ativo"),
            dados["nivel_acessibilidade"],
            dados["observacoes_acesso"],
            dados["data_avaliacao_acesso"],
            dados["responsavel_avaliacao_id"],
            ponto_id,
        ),
    )


def historico(ponto_id, limite=None):
    parametros = [ponto_id]
    limite_sql = ""
    if limite is not None:
        limite_sql = "LIMIT ?"
        parametros.append(limite)
    return database.query_all(
        """
        SELECT * FROM ocorrencias
        WHERE ponto_id = ?
        ORDER BY data_hora DESC
        """ + limite_sql,
        tuple(parametros),
    )


def estatisticas_ocorrencias(ponto_id):
    total = database.query_one(
        """
        SELECT COUNT(*) AS total,
               SUM(CASE WHEN data_hora >= datetime('now', '-90 days') THEN 1 ELSE 0 END) AS recentes
        FROM ocorrencias WHERE ponto_id = ?
        """,
        (ponto_id,),
    )
    ultima = database.query_one(
        """
        SELECT data_hora, nivel_acumulo FROM ocorrencias
        WHERE ponto_id = ? ORDER BY data_hora DESC, id DESC LIMIT 1
        """,
        (ponto_id,),
    )
    foto = database.query_one(
        """
        SELECT fotografia FROM ocorrencias
        WHERE ponto_id = ? AND fotografia IS NOT NULL AND fotografia != ''
        ORDER BY data_hora DESC, id DESC LIMIT 1
        """,
        (ponto_id,),
    )
    distribuicoes = {}
    for campo in ("tipo_residuo", "nivel_acumulo", "status"):
        linhas = database.query_all(
            f"SELECT {campo} AS valor, COUNT(*) AS quantidade FROM ocorrencias "
            f"WHERE ponto_id = ? GROUP BY {campo}",
            (ponto_id,),
        )
        distribuicoes[campo] = {linha["valor"]: linha["quantidade"] for linha in linhas}
    return {
        "total": total["total"],
        "recentes": total["recentes"] or 0,
        "ultima_ocorrencia": ultima["data_hora"] if ultima else None,
        "ultimo_nivel": ultima["nivel_acumulo"] if ultima else None,
        "fotografia_recente": foto["fotografia"] if foto else None,
        "por_tipo": distribuicoes["tipo_residuo"],
        "por_nivel": distribuicoes["nivel_acumulo"],
        "por_status": distribuicoes["status"],
    }
