import base64
import io
import json


def test_listar_ocorrencias(client):
    resp = client.get("/api/ocorrencias")
    assert resp.status_code == 200
    data = resp.get_json()
    assert "ocorrencias" in data
    assert "total" in data


def test_filtrar_ocorrencias_por_tipo(client):
    resp = client.get("/api/ocorrencias?tipo_residuo=Plastico")
    assert resp.status_code == 200
    data = resp.get_json()
    for o in data["ocorrencias"]:
        assert o["tipo_residuo"] == "Plastico"


def test_filtrar_ocorrencias_por_nivel(client):
    resp = client.get("/api/ocorrencias?nivel_acumulo=Alto")
    assert resp.status_code == 200
    data = resp.get_json()
    for o in data["ocorrencias"]:
        assert o["nivel_acumulo"] == "Alto"


def test_filtrar_ocorrencias_por_ponto(client):
    resp = client.get("/api/ocorrencias?ponto_id=1")
    assert resp.status_code == 200
    data = resp.get_json()
    for o in data["ocorrencias"]:
        assert o["ponto_id"] == 1


def test_criar_ocorrencia_sem_auth(client):
    resp = client.post(
        "/api/ocorrencias",
        data={
            "latitude": -3.05,
            "longitude": -60.01,
            "tipo_residuo": "Plastico",
            "nivel_acumulo": "Alto",
        },
    )
    assert resp.status_code == 401


def test_login_usuario_valido(client):
    resp = client.post(
        "/api/auth/login",
        data=json.dumps({"email": "admin@igarape.local", "senha": "admin123"}),
        content_type="application/json",
    )
    assert resp.status_code == 200
    data = resp.get_json()
    assert "usuario" in data
    assert data["usuario"]["email"] == "admin@igarape.local"
    assert "senha_hash" not in data["usuario"]


def test_login_usuario_invalido(client):
    resp = client.post(
        "/api/auth/login",
        data=json.dumps({"email": "admin@igarape.local", "senha": "errada"}),
        content_type="application/json",
    )
    assert resp.status_code == 401


def test_login_nao_aceita_json_que_nao_seja_objeto(client):
    resp = client.post("/api/auth/login", json=["valor-invalido"])
    assert resp.status_code == 400


def test_dashboard_resumo(client):
    resp = client.get("/api/dashboard/resumo")
    assert resp.status_code == 200
    data = resp.get_json()
    assert "total_ocorrencias" in data
    assert "pontos_monitorados" in data


def test_exportar_csv(client):
    resp = client.get("/api/export/ocorrencias.csv")
    assert resp.status_code == 200
    assert resp.content_type == "text/csv; charset=utf-8"


def test_exportar_geojson(client):
    resp = client.get("/api/export/ocorrencias.geojson")
    assert resp.status_code == 200
    assert resp.content_type == "application/json"
    data = resp.get_json()
    assert data["type"] == "FeatureCollection"


def test_pagina_inicial(client):
    resp = client.get("/")
    assert resp.status_code == 200
    assert b"Mapa" in resp.data


def test_pagina_dashboard(client):
    resp = client.get("/dashboard")
    assert resp.status_code == 200
    assert b"Dashboard" in resp.data


def test_pagina_login(client):
    resp = client.get("/login")
    assert resp.status_code == 200
    assert b"Login" in resp.data


def _login(client):
    return client.post(
        "/api/auth/login",
        json={"email": "admin@igarape.local", "senha": "admin123"},
    )


def test_api_publica_nao_expoe_usuario_id(client):
    resp = client.get("/api/ocorrencias")
    assert resp.status_code == 200
    for ocorrencia in resp.get_json()["ocorrencias"]:
        assert "usuario_id" not in ocorrencia


def test_rejeita_arquivo_falso_com_extensao_de_imagem(client):
    assert _login(client).status_code == 200
    resp = client.post(
        "/api/ocorrencias",
        data={
            "latitude": "-3.05",
            "longitude": "-60.01",
            "tipo_residuo": "Plastico",
            "nivel_acumulo": "Alto",
            "fotografia": (io.BytesIO(b"isto nao e uma imagem"), "foto.jpg"),
        },
        content_type="multipart/form-data",
    )
    assert resp.status_code == 400


def test_permite_ocorrencia_sem_fotografia(client):
    assert _login(client).status_code == 200
    resp = client.post(
        "/api/ocorrencias",
        data={
            "latitude": "-3.05",
            "longitude": "-60.01",
            "tipo_residuo": "Plastico",
            "nivel_acumulo": "Alto",
        },
    )
    assert resp.status_code == 201


def test_permite_imagem_png_valida(client):
    assert _login(client).status_code == 200
    png = base64.b64decode(
        "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNk+A8AAQUBAScY42YAAAAASUVORK5CYII="
    )
    resp = client.post(
        "/api/ocorrencias",
        data={
            "latitude": "-3.05",
            "longitude": "-60.01",
            "tipo_residuo": "Plastico",
            "nivel_acumulo": "Alto",
            "fotografia": (io.BytesIO(png), "foto.png"),
        },
        content_type="multipart/form-data",
    )
    assert resp.status_code == 201


def test_limite_de_upload_retorna_413(client):
    assert _login(client).status_code == 200
    client.application.config["MAX_CONTENT_LENGTH"] = 512
    resp = client.post(
        "/api/ocorrencias",
        data={
            "latitude": "-3.05",
            "longitude": "-60.01",
            "tipo_residuo": "Plastico",
            "nivel_acumulo": "Alto",
            "fotografia": (io.BytesIO(b"x" * 2048), "foto.png"),
        },
        content_type="multipart/form-data",
    )
    assert resp.status_code == 413


def test_cabecalhos_de_seguranca(client):
    resp = client.get("/")
    assert resp.headers["X-Content-Type-Options"] == "nosniff"
    assert resp.headers["X-Frame-Options"] == "SAMEORIGIN"
