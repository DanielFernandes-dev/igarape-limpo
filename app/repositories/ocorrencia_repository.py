import database


def listar_todas(filtros=None):
    sql = "SELECT * FROM ocorrencias"
    clausulas, parametros = _construir_filtros(filtros or {})
    if clausulas:
        sql += " WHERE " + " AND ".join(clausulas)
    sql += " ORDER BY data_hora DESC"
    return database.query_all(sql, parametros)


def contar(filtros=None):
    sql = "SELECT COUNT(*) FROM ocorrencias"
    clausulas, parametros = _construir_filtros(filtros or {})
    if clausulas:
        sql += " WHERE " + " AND ".join(clausulas)
    return database.query_one(sql, parametros)[0]


def _construir_filtros(filtros):
    clausulas = []
    parametros = []

    if filtros.get("tipo_residuo"):
        clausulas.append("tipo_residuo = ?")
        parametros.append(filtros["tipo_residuo"])
    if filtros.get("nivel_acumulo"):
        clausulas.append("nivel_acumulo = ?")
        parametros.append(filtros["nivel_acumulo"])
    if filtros.get("ponto_id") is not None:
        clausulas.append("ponto_id = ?")
        parametros.append(filtros["ponto_id"])
    if filtros.get("data_inicio"):
        clausulas.append("data_hora >= ?")
        parametros.append(filtros["data_inicio"])
    if filtros.get("data_fim"):
        clausulas.append("data_hora <= ?")
        parametros.append(filtros["data_fim"])
    if filtros.get("busca"):
        clausulas.append("(local_nome LIKE ? OR observacoes LIKE ?)")
        termo = f"%{filtros['busca']}%"
        parametros.extend([termo, termo])

    return clausulas, parametros


def obter_por_id(ocorrencia_id):
    return database.query_one(
        "SELECT * FROM ocorrencias WHERE id = ?", (ocorrencia_id,)
    )


def criar(dados):
    return database.query_insert(
        """
        INSERT INTO ocorrencias
            (ponto_id, usuario_id, latitude, longitude, fotografia, tipo_residuo, nivel_acumulo,
             status, observacoes, local_nome)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            dados.get("ponto_id"),
            dados.get("usuario_id"),
            dados["latitude"],
            dados["longitude"],
            dados.get("fotografia"),
            dados["tipo_residuo"],
            dados["nivel_acumulo"],
            dados.get("status", "Nova"),
            dados.get("observacoes"),
            dados.get("local_nome"),
        ),
    )


def atualizar(ocorrencia_id, dados):
    return database.query_update(
        """
        UPDATE ocorrencias
        SET ponto_id = ?, latitude = ?, longitude = ?, fotografia = ?, tipo_residuo = ?,
            nivel_acumulo = ?, status = ?, observacoes = ?, local_nome = ?,
            data_atualizacao = datetime('now')
        WHERE id = ?
        """,
        (
            dados.get("ponto_id"),
            dados["latitude"],
            dados["longitude"],
            dados.get("fotografia"),
            dados["tipo_residuo"],
            dados["nivel_acumulo"],
            dados.get("status", "Nova"),
            dados.get("observacoes"),
            dados.get("local_nome"),
            ocorrencia_id,
        ),
    )


def excluir(ocorrencia_id):
    return database.query_update(
        "DELETE FROM ocorrencias WHERE id = ?", (ocorrencia_id,)
    )

