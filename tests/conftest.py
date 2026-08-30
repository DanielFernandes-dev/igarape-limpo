import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pytest

import config
import database
from app import create_app


@pytest.fixture
def client(tmp_path, monkeypatch):
    banco_teste = tmp_path / "teste.db"
    uploads_teste = tmp_path / "uploads"
    monkeypatch.setattr(database, "DATABASE_PATH", str(banco_teste))
    monkeypatch.setattr(config, "DATABASE_PATH", str(banco_teste))
    monkeypatch.setattr(config, "UPLOAD_FOLDER", str(uploads_teste))

    app = create_app()
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client
