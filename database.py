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
                    ('Igarapé do Educandos — Foz', -3.140000, -60.008000, 'Desembocadura do igarapé.', 'Ativo');
                """
            )
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
