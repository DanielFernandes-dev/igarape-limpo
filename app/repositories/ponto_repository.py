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
        "SELECT * FROM pontos_monitorados WHERE id = ?", (ponto_id,)
    )


def criar(dados):
    return database.query_insert(
        """
        INSERT INTO pontos_monitorados (nome, latitude, longitude, descricao, status)
        VALUES (?, ?, ?, ?, ?)
        """,
        (
            dados["nome"],
            dados["latitude"],
            dados["longitude"],
            dados.get("descricao"),
            dados.get("status", "Ativo"),
        ),
    )


def atualizar(ponto_id, dados):
    return database.query_update(
        """
        UPDATE pontos_monitorados
        SET nome = ?, latitude = ?, longitude = ?, descricao = ?, status = ?
        WHERE id = ?
        """,
        (
            dados["nome"],
            dados["latitude"],
            dados["longitude"],
            dados.get("descricao"),
            dados.get("status", "Ativo"),
            ponto_id,
        ),
    )


def historico(ponto_id, limite=50):
    return database.query_all(
        """
        SELECT * FROM ocorrencias
        WHERE ponto_id = ?
        ORDER BY data_hora DESC
        LIMIT ?
        """,
        (ponto_id, limite),
    )
