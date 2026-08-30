import os
import sqlite3

from flask import g

from config import DATABASE_PATH, SCHEMA_PATH


def get_db():
    if "db" not in g:
        g.db = sqlite3.connect(DATABASE_PATH)
        g.db.row_factory = sqlite3.Row
    return g.db


def close_db(e=None):
    db = g.pop("db", None)
    if db is not None:
        db.close()


def init_app(app):
    app.teardown_appcontext(close_db)


def init_db():
    db = sqlite3.connect(DATABASE_PATH)
    with open(SCHEMA_PATH, "r", encoding="utf-8") as f:
        db.executescript(f.read())
    db.commit()
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
