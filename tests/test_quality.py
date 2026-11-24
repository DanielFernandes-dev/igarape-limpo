import base64
import io
import json
import sqlite3

import database


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


def test_dashboard_comparacao(client):
    resp = client.get("/api/dashboard/comparacao?dias=7")
    assert resp.status_code == 200
    data = resp.get_json()
    assert "periodo_atual" in data
    assert "periodo_anterior" in data
    assert "alerta" in data


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


def test_painel_operador_exige_perfil_elevado(client):
    assert client.get("/operador").status_code == 302
    assert _login(client).status_code == 200
    resp = client.get("/operador")
    assert resp.status_code == 200
    assert b"Painel de operador" in resp.data


def test_pagina_login(client):
    resp = client.get("/login")
    assert resp.status_code == 200
    assert b"Login" in resp.data


def test_cadastro_publico_cria_usuario_com_perfil_comum(client):
    pagina = client.get("/cadastro")
    assert pagina.status_code == 200
    resp = client.post(
        "/api/auth/cadastro",
        json={
            "nome": "Participante novo",
            "email": "participante@example.com",
            "senha": "senha123",
            "perfil": "administrador",
        },
    )
    assert resp.status_code == 201
    login = client.post(
        "/api/auth/login",
        json={"email": "participante@example.com", "senha": "senha123"},
    )
    assert login.status_code == 200
    assert login.get_json()["usuario"]["perfil"] == "usuario"


def test_cadastro_rejeita_email_existente(client):
    resp = client.post(
        "/api/auth/cadastro",
        json={"nome": "Admin duplicado", "email": "admin@igarape.local", "senha": "senha123"},
    )
    assert resp.status_code == 409


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


def test_patch_parcial_de_ocorrencia_sem_campos_opcionais(client):
    assert _login(client).status_code == 200
    criada = client.post(
        "/api/ocorrencias",
        data={
            "latitude": "-3.05",
            "longitude": "-60.01",
            "tipo_residuo": "Plastico",
            "nivel_acumulo": "Alto",
        },
    )
    assert criada.status_code == 201
    assert client.patch(
        f"/api/ocorrencias/{criada.get_json()['id']}",
        json={"status": "Resolvida"},
    ).status_code == 200


def test_rejeita_payloads_json_que_nao_sejam_objetos(client):
    assert _login(client).status_code == 200
    assert client.patch("/api/ocorrencias/1", json=["status"]).status_code == 400
    assert client.post("/api/integracao/sensores", json=["url"]).status_code == 400


def test_rejeita_coordenadas_invalidas_nas_integracoes(client):
    assert client.get("/api/integracao/meteo?lat=abc&lon=-60").status_code == 400
    assert client.get("/api/integracao/geocode?lat=nan&lon=-60").status_code == 400
    assert client.get("/api/integracao/meteo?lat=91&lon=-60").status_code == 400


def test_csv_neutraliza_formulas_de_planilha(client):
    assert _login(client).status_code == 200
    criada = client.post(
        "/api/ocorrencias",
        data={
            "latitude": "-3.05",
            "longitude": "-60.01",
            "tipo_residuo": "Plastico",
            "nivel_acumulo": "Alto",
            "observacoes": "=HYPERLINK(\"https://example.com\")",
        },
    )
    assert criada.status_code == 201
    csv = client.get("/api/export/ocorrencias.csv").get_data(as_text=True)
    assert "'=HYPERLINK" in csv


def test_usuario_nao_edita_ocorrencia_de_outro_usuario(client):
    assert _login(client).status_code == 200
    criada = client.post(
        "/api/ocorrencias",
        data={
            "latitude": "-3.05",
            "longitude": "-60.01",
            "tipo_residuo": "Plastico",
            "nivel_acumulo": "Alto",
        },
    )
    assert criada.status_code == 201
    criado_id = criada.get_json()["id"]
    usuario = client.post(
        "/api/auth/usuarios",
        json={"nome": "Colaborador", "email": "colaborador@teste.local", "senha": "senha123"},
    )
    assert usuario.status_code == 201
    client.post("/api/auth/logout")
    assert client.post(
        "/api/auth/login",
        json={"email": "colaborador@teste.local", "senha": "senha123"},
    ).status_code == 200
    assert client.patch(
        f"/api/ocorrencias/{criado_id}",
        json={"status": "Resolvida"},
    ).status_code == 403


def test_gateway_nao_acessa_endereco_local(client):
    assert _login(client).status_code == 200
    resposta = client.post(
        "/api/integracao/sensores",
        json={"url": "http://localhost:8080/estacoes"},
    )
    assert resposta.status_code == 502


def test_acessibilidade_ponto_e_filtro(client):
    assert _login(client).status_code == 200
    resposta = client.patch(
        "/api/pontos/1",
        json={
            "nome": "Igarapé do Mindu — Trecho 1",
            "latitude": -3.059860,
            "longitude": -60.040980,
            "descricao": "Margem próxima à passarela.",
            "status": "Ativo",
            "nivel_acessibilidade": "Dificultoso",
            "observacoes_acesso": "Acesso depende de equipamento.",
            "data_avaliacao_acesso": "2026-11-24T10:00",
        },
    )
    assert resposta.status_code == 200
    ponto = client.get("/api/pontos/1").get_json()
    assert ponto["nivel_acessibilidade"] == "Dificultoso"
    assert ponto["observacoes_acesso"] == "Acesso depende de equipamento."
    assert client.get("/api/pontos?acessibilidade=Dificultoso").status_code == 200


def test_acessibilidade_rejeita_nivel_invalido(client):
    assert _login(client).status_code == 200
    resposta = client.patch(
        "/api/pontos/1",
        json={"nivel_acessibilidade": "Impossivel"},
    )
    assert resposta.status_code == 400


def test_usuario_comum_nao_altera_acessibilidade(client):
    assert _login(client).status_code == 200
    assert client.post(
        "/api/auth/usuarios",
        json={"nome": "Morador", "email": "morador@teste.local", "senha": "senha123"},
    ).status_code == 201
    client.post("/api/auth/logout")
    assert client.post(
        "/api/auth/login",
        json={"email": "morador@teste.local", "senha": "senha123"},
    ).status_code == 200
    assert client.patch(
        "/api/pontos/1",
        json={"nivel_acessibilidade": "Dificultoso"},
    ).status_code == 403


def test_limpeza_reincidencia_e_permissao(client):
    assert client.post(
        "/api/pontos/1/limpezas",
        data={"data_hora": "2026-11-10T12:00", "equipe": "Equipe A"},
    ).status_code == 401
    assert _login(client).status_code == 200
    limpeza = client.post(
        "/api/pontos/1/limpezas",
        data={
            "data_hora": "2026-11-10T12:00",
            "equipe": "Equipe A",
            "quantidade": "25",
            "unidade": "kg",
        },
    )
    assert limpeza.status_code == 201
    nova = client.post(
        "/api/ocorrencias",
        data={
            "ponto_id": "1",
            "latitude": "-3.059860",
            "longitude": "-60.040980",
            "tipo_residuo": "Plastico",
            "nivel_acumulo": "Alto",
        },
    )
    assert nova.status_code == 201
    with client.application.app_context():
        database.query_update(
            "UPDATE ocorrencias SET data_hora = ? WHERE id = ?",
            ("2026-11-10 13:00:00", nova.get_json()["id"]),
        )
    resumo = client.get("/api/pontos/1").get_json()
    assert resumo["total_limpezas"] >= 1
    assert resumo["novas_ocorrencias_apos_limpeza"] >= 1
    assert resumo["houve_reincidencia"] is True
    assert client.patch(
        f"/api/ocorrencias/{nova.get_json()['id']}",
        json={"status": "Resolvida"},
    ).status_code == 200
    assert client.get("/api/pontos/1").get_json()["novas_ocorrencias_apos_limpeza"] >= 1


def test_protocolo_unico_e_acompanhamento_publico(client):
    assert _login(client).status_code == 200
    primeira = client.post(
        "/api/ocorrencias",
        data={
            "ponto_id": "1",
            "latitude": "-3.059860",
            "longitude": "-60.040980",
            "tipo_residuo": "Plastico",
            "nivel_acumulo": "Medio",
        },
    )
    segunda = client.post(
        "/api/ocorrencias",
        data={
            "ponto_id": "1",
            "latitude": "-3.059860",
            "longitude": "-60.040980",
            "tipo_residuo": "Vidro",
            "nivel_acumulo": "Baixo",
        },
    )
    assert primeira.status_code == 201
    assert segunda.status_code == 201
    protocolo1 = primeira.get_json()["protocolo"]
    protocolo2 = segunda.get_json()["protocolo"]
    assert protocolo1.startswith("IG-")
    assert protocolo2.startswith("IG-")
    assert protocolo1 != protocolo2
    client.post("/api/auth/logout")
    consulta = client.get(f"/api/denuncias/{protocolo1}")
    assert consulta.status_code == 200
    assert "usuario_id" not in consulta.get_json()["denuncia"]


def test_migracao_preserva_dados_existentes(client, tmp_path, monkeypatch):
    banco = tmp_path / "legado.db"
    conexao = sqlite3.connect(banco)
    conexao.executescript(
        """
        CREATE TABLE usuarios (
            id INTEGER PRIMARY KEY, nome TEXT, email TEXT, senha_hash TEXT,
            perfil TEXT, ativo INTEGER
        );
        CREATE TABLE pontos_monitorados (
            id INTEGER PRIMARY KEY, nome TEXT, latitude REAL, longitude REAL,
            descricao TEXT, status TEXT
        );
        CREATE TABLE ocorrencias (
            id INTEGER PRIMARY KEY, ponto_id INTEGER, usuario_id INTEGER,
            latitude REAL, longitude REAL, data_hora TEXT, fotografia TEXT,
            tipo_residuo TEXT, nivel_acumulo TEXT, status TEXT, observacoes TEXT,
            local_nome TEXT, data_atualizacao TEXT
        );
        INSERT INTO usuarios VALUES (7, 'Legado', 'legado@teste.local', 'hash', 'usuario', 1);
        INSERT INTO pontos_monitorados VALUES (9, 'Trecho legado', -3.1, -60.1, NULL, 'Ativo');
        INSERT INTO ocorrencias VALUES
            (12, 9, 7, -3.1, -60.1, '2026-11-01 10:00:00', NULL, 'Plastico', 'Alto', 'Nova', NULL, 'Mindu', NULL);
        """
    )
    conexao.commit()
    conexao.close()
    monkeypatch.setattr(database, "DATABASE_PATH", str(banco))
    database.migrar()
    verificacao = sqlite3.connect(banco)
    assert verificacao.execute("SELECT id, email FROM usuarios").fetchone() == (7, "legado@teste.local")
    assert verificacao.execute("SELECT id, nome FROM pontos_monitorados").fetchone() == (9, "Trecho legado")
    protocolo = verificacao.execute("SELECT protocolo FROM ocorrencias WHERE id = 12").fetchone()[0]
    assert protocolo.startswith("IG-2026-")
    assert verificacao.execute("SELECT COUNT(*) FROM limpezas").fetchone()[0] == 0
    verificacao.close()
