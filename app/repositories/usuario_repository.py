import database


def listar_todos():
    return database.query_all(
        """
        SELECT id, nome, email, perfil, ativo, data_criacao
        FROM usuarios
        ORDER BY nome
        """
    )


def obter_por_id(usuario_id):
    return database.query_one(
        "SELECT id, nome, email, perfil, ativo, data_criacao FROM usuarios WHERE id = ?",
        (usuario_id,),
    )


def obter_por_email(email):
    return database.query_one(
        "SELECT * FROM usuarios WHERE email = ?",
        (email,),
    )


def criar(dados):
    return database.query_insert(
        """
        INSERT INTO usuarios (nome, email, senha_hash, perfil, ativo)
        VALUES (?, ?, ?, ?, ?)
        """,
        (
            dados["nome"],
            dados["email"],
            dados["senha_hash"],
            dados.get("perfil", "usuario"),
            dados.get("ativo", 1),
        ),
    )


def atualizar(usuario_id, dados):
    return database.query_update(
        """
        UPDATE usuarios
        SET nome = ?, email = ?, perfil = ?, ativo = ?
        WHERE id = ?
        """,
        (
            dados["nome"],
            dados["email"],
            dados.get("perfil", "usuario"),
            dados.get("ativo", 1),
            usuario_id,
        ),
    )


def atualizar_senha(usuario_id, senha_hash):
    return database.query_update(
        "UPDATE usuarios SET senha_hash = ? WHERE id = ?",
        (senha_hash, usuario_id),
    )


def excluir(usuario_id):
    return database.query_update(
        "DELETE FROM usuarios WHERE id = ?",
        (usuario_id,),
    )
