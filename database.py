import fcntl
import os
import sqlite3

from flask import g

from config import DATABASE_PATH, SCHEMA_PATH


def get_db():
    if "db" not in g:
        g.db = sqlite3.connect(DATABASE_PATH)
        g.db.row_factory = sqlite3.Row
        g.db.execute("PRAGMA foreign_keys = ON")
    return g.db


def close_db(e=None):
    db = g.pop("db", None)
    if db is not None:
        db.close()


def init_app(app):
    app.teardown_appcontext(close_db)

    os.makedirs(os.path.dirname(DATABASE_PATH), exist_ok=True)
    lock_path = DATABASE_PATH + ".lock"
    with open(lock_path, "w") as lock:
        fcntl.flock(lock, fcntl.LOCK_EX)
        try:
            if not os.path.exists(DATABASE_PATH):
                init_db()
            else:
                migrar()
        finally:
            fcntl.flock(lock, fcntl.LOCK_UN)


def init_db():
    db = sqlite3.connect(DATABASE_PATH)
    with open(SCHEMA_PATH, "r", encoding="utf-8") as f:
        db.executescript(f.read())
    registros = db.execute(
        "SELECT id, data_hora FROM ocorrencias WHERE protocolo IS NULL OR protocolo = ''"
    ).fetchall()
    for numero, registro in enumerate(registros, start=1):
        ano = str(registro[1] or "2026")[:4]
        db.execute(
            "UPDATE ocorrencias SET protocolo = ? WHERE id = ?",
            (f"IG-{ano}-{numero:06d}", registro[0]),
        )
    db.commit()

    from app.services.auth_service import hash_senha

    admin_hash = hash_senha("admin123")
    db.execute(
        """
        INSERT OR IGNORE INTO usuarios (nome, email, senha_hash, perfil, ativo)
        VALUES ('Administrador', 'admin@igarape.local', ?, 'administrador', 1)
        """,
        (admin_hash,),
    )
    db.commit()
    db.close()


def migrar():
    """Aplica evoluções de schema em bancos já existentes (idempotente)."""
    db = sqlite3.connect(DATABASE_PATH)
    db.row_factory = sqlite3.Row
    try:
        db.execute("PRAGMA foreign_keys = ON")
        db.executescript(
            """
            CREATE TABLE IF NOT EXISTS usuarios (
                id INTEGER PRIMARY KEY AUTOINCREMENT, nome TEXT NOT NULL,
                email TEXT NOT NULL UNIQUE, senha_hash TEXT NOT NULL,
                perfil TEXT NOT NULL DEFAULT 'usuario', ativo INTEGER NOT NULL DEFAULT 1,
                data_criacao TEXT NOT NULL DEFAULT (datetime('now'))
            );
            CREATE TABLE IF NOT EXISTS pontos_monitorados (
                id INTEGER PRIMARY KEY AUTOINCREMENT, nome TEXT NOT NULL,
                latitude REAL NOT NULL, longitude REAL NOT NULL, descricao TEXT,
                status TEXT NOT NULL DEFAULT 'Ativo',
                data_criacao TEXT NOT NULL DEFAULT (datetime('now'))
            );
            CREATE TABLE IF NOT EXISTS ocorrencias (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                ponto_id INTEGER REFERENCES pontos_monitorados (id),
                usuario_id INTEGER REFERENCES usuarios (id), latitude REAL NOT NULL,
                longitude REAL NOT NULL, data_hora TEXT NOT NULL DEFAULT (datetime('now')),
                fotografia TEXT, tipo_residuo TEXT NOT NULL, nivel_acumulo TEXT NOT NULL,
                status TEXT NOT NULL DEFAULT 'Nova', observacoes TEXT, local_nome TEXT,
                data_atualizacao TEXT
            );
            """
        )
        colunas = {r[1] for r in db.execute("PRAGMA table_info(ocorrencias)")}
        if "ponto_id" not in colunas:
            db.execute(
                "ALTER TABLE ocorrencias ADD COLUMN ponto_id INTEGER REFERENCES pontos_monitorados (id)"
            )
        if "status" not in colunas:
            db.execute(
                "ALTER TABLE ocorrencias ADD COLUMN status TEXT NOT NULL DEFAULT 'Nova'"
            )
        if "data_atualizacao" not in colunas:
            db.execute("ALTER TABLE ocorrencias ADD COLUMN data_atualizacao TEXT")
        if "usuario_id" not in colunas:
            db.execute(
                "ALTER TABLE ocorrencias ADD COLUMN usuario_id INTEGER REFERENCES usuarios (id)"
            )
        if "protocolo" not in colunas:
            db.execute("ALTER TABLE ocorrencias ADD COLUMN protocolo TEXT")
        colunas_pontos = {r[1] for r in db.execute("PRAGMA table_info(pontos_monitorados)")}
        if "nivel_acessibilidade" not in colunas_pontos:
            db.execute("ALTER TABLE pontos_monitorados ADD COLUMN nivel_acessibilidade TEXT")
        if "observacoes_acesso" not in colunas_pontos:
            db.execute("ALTER TABLE pontos_monitorados ADD COLUMN observacoes_acesso TEXT")
        if "data_avaliacao_acesso" not in colunas_pontos:
            db.execute("ALTER TABLE pontos_monitorados ADD COLUMN data_avaliacao_acesso TEXT")
        if "responsavel_avaliacao_id" not in colunas_pontos:
            db.execute(
                "ALTER TABLE pontos_monitorados ADD COLUMN responsavel_avaliacao_id INTEGER "
                "REFERENCES usuarios (id)"
            )

        db.executescript(
            """
            CREATE TABLE IF NOT EXISTS limpezas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                ponto_id INTEGER NOT NULL REFERENCES pontos_monitorados (id) ON DELETE CASCADE,
                data_hora TEXT NOT NULL,
                equipe TEXT,
                quantidade REAL,
                unidade TEXT,
                fotografia TEXT,
                observacoes TEXT,
                usuario_id INTEGER REFERENCES usuarios (id),
                data_cadastro TEXT NOT NULL DEFAULT (datetime('now'))
            );
            CREATE INDEX IF NOT EXISTS idx_limpezas_ponto_data
            ON limpezas (ponto_id, data_hora DESC);
            CREATE INDEX IF NOT EXISTS idx_ocorrencias_ponto_data
            ON ocorrencias (ponto_id, data_hora DESC);
            CREATE INDEX IF NOT EXISTS idx_ocorrencias_protocolo
            ON ocorrencias (protocolo);
            CREATE UNIQUE INDEX IF NOT EXISTS idx_ocorrencias_protocolo_unico
            ON ocorrencias (protocolo) WHERE protocolo IS NOT NULL;
            """
        )

        sem_protocolo = db.execute(
            "SELECT id, data_hora FROM ocorrencias WHERE protocolo IS NULL OR protocolo = ''"
        ).fetchall()
        for registro in sem_protocolo:
            ano = str(registro["data_hora"] or "2026")[:4]
            candidato = f"IG-{ano}-{registro['id']:06d}"
            contador = registro["id"]
            while db.execute(
                "SELECT 1 FROM ocorrencias WHERE protocolo = ?", (candidato,)
            ).fetchone():
                contador += 1
                candidato = f"IG-{ano}-{contador:06d}"
            db.execute(
                "UPDATE ocorrencias SET protocolo = ? WHERE id = ?",
                (candidato, registro["id"]),
            )

        db.execute(
            """
            CREATE TABLE IF NOT EXISTS pontos_monitorados (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                latitude REAL NOT NULL,
                longitude REAL NOT NULL,
                descricao TEXT,
                status TEXT NOT NULL DEFAULT 'Ativo',
                data_criacao TEXT NOT NULL DEFAULT (datetime('now'))
            )
            """
        )

        db.execute(
            """
            CREATE TABLE IF NOT EXISTS usuarios (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                email TEXT NOT NULL UNIQUE,
                senha_hash TEXT NOT NULL,
                perfil TEXT NOT NULL DEFAULT 'usuario',
                ativo INTEGER NOT NULL DEFAULT 1,
                data_criacao TEXT NOT NULL DEFAULT (datetime('now'))
            )
            """
        )
        db.commit()

        vazio = db.execute("SELECT COUNT(*) FROM pontos_monitorados").fetchone()[0]
        if vazio == 0:
            db.executescript(
                """
                INSERT INTO pontos_monitorados (nome, latitude, longitude, descricao, status)
                VALUES
                    ('Igarapé do Mindu — Trecho 1', -3.059860, -60.040980, 'Margem próxima à passarela.', 'Ativo'),
                    ('Igarapé do Mindu — Trecho 2', -3.057500, -60.047000, 'Ponte central, ponto de descarte frequente.', 'Ativo'),
                    ('Igarapé do Educandos — Foz', -3.140000, -60.008000, 'Desembocadura do igarapé.', 'Ativo'),
                    ('Igarapé do Quarenta — Trecho demonstrativo', -3.1307664, -59.9964426, 'Coordenada de referência do OpenStreetMap; validar em campo.', 'Ativo'),
                    ('Igarapé Tarumã-Açu — Trecho demonstrativo', -2.9858251, -60.1261855, 'Coordenada de referência do OpenStreetMap; validar em campo.', 'Ativo');
                """
            )
            db.commit()

        _migrar_ocorrencias_demo_igarapes(db)
        db.commit()

        usuario_vazio = db.execute("SELECT COUNT(*) FROM usuarios").fetchone()[0]
        if usuario_vazio == 0:
            from app.services.auth_service import hash_senha

            admin_hash = hash_senha("admin123")
            db.execute(
                """
                INSERT OR IGNORE INTO usuarios (nome, email, senha_hash, perfil, ativo)
                VALUES ('Administrador', 'admin@igarape.local', ?, 'administrador', 1)
                """,
                (admin_hash,),
            )
            db.commit()
    except sqlite3.Error:
        db.rollback()
        raise
    finally:
        db.close()


def _migrar_ocorrencias_demo_igarapes(db):
    exemplos = (
        (
            "2026-08-25 14:30:00",
            -3.058412,
            -60.045120,
            "Misto",
            "Medio",
            "Em analise",
            "Garrafas pet e embalagens espalhadas.",
            "Igarapé do Quarenta — Trecho demonstrativo",
            "Igarapé do Quarenta",
        ),
        (
            "2026-08-26 10:05:00",
            -3.061230,
            -60.038500,
            "Metal",
            "Baixo",
            "Resolvida",
            "Poucas latas e ferros velhos.",
            "Igarapé Tarumã-Açu — Trecho demonstrativo",
            "Igarapé Tarumã-Açu",
        ),
        (
            "2026-08-28 16:20:00",
            -3.057500,
            -60.047000,
            "Vidro",
            "Medio",
            "Nova",
            "Garrafas de vidro quebradas.",
            "Igarapé do Quarenta — Trecho demonstrativo",
            "Igarapé do Quarenta",
        ),
    )
    encontrados = []
    for exemplo in exemplos:
        (
            data_hora,
            latitude,
            longitude,
            tipo_residuo,
            nivel_acumulo,
            status,
            observacoes,
            nome_ponto,
            local_nome,
        ) = exemplo
        registro = db.execute(
            """
            SELECT id FROM ocorrencias
            WHERE usuario_id IS NULL AND ponto_id IN (1, 2)
                AND data_hora = ? AND latitude = ? AND longitude = ?
                AND tipo_residuo = ? AND nivel_acumulo = ? AND status = ?
                AND observacoes = ? AND local_nome = 'Igarapé do Mindu'
                AND fotografia IS NULL
            """,
            (
                data_hora,
                latitude,
                longitude,
                tipo_residuo,
                nivel_acumulo,
                status,
                observacoes,
            ),
        ).fetchone()
        if registro:
            encontrados.append((registro["id"], nome_ponto, local_nome))

    if not encontrados:
        return

    coordenadas = {
        "Igarapé do Quarenta — Trecho demonstrativo": (
            -3.1307664,
            -59.9964426,
        ),
        "Igarapé Tarumã-Açu — Trecho demonstrativo": (
            -2.9858251,
            -60.1261855,
        ),
    }
    pontos_destino = {}
    for nome_ponto in {nome for _, nome, _ in encontrados}:
        ponto = db.execute(
            "SELECT id, latitude, longitude FROM pontos_monitorados WHERE nome = ?",
            (nome_ponto,),
        ).fetchone()
        if ponto is None:
            latitude, longitude = coordenadas[nome_ponto]
            cursor = db.execute(
                """
                INSERT INTO pontos_monitorados
                    (nome, latitude, longitude, descricao, status)
                VALUES (?, ?, ?, ?, 'Ativo')
                """,
                (
                    nome_ponto,
                    latitude,
                    longitude,
                    "Coordenada de referência do OpenStreetMap; validar em campo.",
                ),
            )
            ponto = {
                "id": cursor.lastrowid,
                "latitude": latitude,
                "longitude": longitude,
            }
        pontos_destino[nome_ponto] = ponto

    for ocorrencia_id, nome_ponto, local_nome in encontrados:
        ponto = pontos_destino[nome_ponto]
        db.execute(
            """
            UPDATE ocorrencias
            SET ponto_id = ?, latitude = ?, longitude = ?, local_nome = ?
            WHERE id = ?
            """,
            (ponto["id"], ponto["latitude"], ponto["longitude"], local_nome, ocorrencia_id),
        )


def query_all(sql, params=()):
    return get_db().execute(sql, params).fetchall()


def query_one(sql, params=()):
    return get_db().execute(sql, params).fetchone()


def query_insert(sql, params=()):
    db = get_db()
    cur = db.execute(sql, params)
    db.commit()
    return cur.lastrowid


def query_update(sql, params=()):
    db = get_db()
    cur = db.execute(sql, params)
    db.commit()
    return cur.rowcount
