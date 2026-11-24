import database


def listar_por_ponto(ponto_id):
    return database.query_all(
        """
        SELECT l.*
        FROM limpezas l
        WHERE l.ponto_id = ?
        ORDER BY l.data_hora DESC, l.id DESC
        """,
        (ponto_id,),
    )


def contar_por_ponto(ponto_id):
    return database.query_one(
        "SELECT COUNT(*) FROM limpezas WHERE ponto_id = ?", (ponto_id,)
    )[0]


def ultima_por_ponto(ponto_id):
    return database.query_one(
        "SELECT * FROM limpezas WHERE ponto_id = ? ORDER BY data_hora DESC, id DESC LIMIT 1",
        (ponto_id,),
    )


def criar(dados):
    return database.query_insert(
        """
        INSERT INTO limpezas
            (ponto_id, data_hora, equipe, quantidade, unidade, fotografia, observacoes, usuario_id)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            dados["ponto_id"], dados["data_hora"], dados.get("equipe"),
            dados.get("quantidade"), dados.get("unidade"), dados.get("fotografia"),
            dados.get("observacoes"), dados.get("usuario_id"),
        ),
    )


def contar_todas():
    return database.query_one("SELECT COUNT(*) FROM limpezas")[0]
