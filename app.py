import os
import uuid

from flask import Flask, jsonify, render_template, request, url_for

import database
from config import (
    ALLOWED_EXTENSIONS,
    COR_NIVEIS,
    MAX_CONTENT_LENGTH,
    NIVEIS_ACUMULO,
    TIPOS_RESIDUO,
    UPLOAD_FOLDER,
)


def create_app():
    app = Flask(__name__)
    app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
    app.config["MAX_CONTENT_LENGTH"] = MAX_CONTENT_LENGTH

    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    database.init_app(app)

    if not os.path.exists(database.DATABASE_PATH):
        database.init_db()

    @app.context_processor
    def inject_constants():
        return {
            "tipos_residuo": TIPOS_RESIDUO,
            "niveis_acumulo": NIVEIS_ACUMULO,
            "cor_niveis": COR_NIVEIS,
        }

    @app.route("/")
    def index():
        return render_template("index.html")

    @app.route("/nova")
    def nova():
        return render_template("nova_ocorrencia.html")

    @app.route("/ocorrencia/<int:ocorrencia_id>")
    def detalhe(ocorrencia_id):
        o = database.query_one(
            "SELECT * FROM ocorrencias WHERE id = ?", (ocorrencia_id,)
        )
        if o is None:
            return render_template("nao_encontrado.html"), 404
        return render_template("ocorrencia.html", o=o)

    @app.route("/api/ocorrencias")
    def listar_ocorrencias():
        rows = database.query_all(
            "SELECT * FROM ocorrencias ORDER BY data_hora DESC"
        )
        resultados = []
        for r in rows:
            item = dict(r)
            item["fotografia"] = (
                url_for("static", filename="uploads/" + r["fotografia"])
                if r["fotografia"]
                else None
            )
            item["cor"] = COR_NIVEIS.get(r["nivel_acumulo"], "#64748b")
            resultados.append(item)
        return jsonify(resultados)

    @app.route("/api/ocorrencias/<int:ocorrencia_id>")
    def obter_ocorrencia(ocorrencia_id):
        r = database.query_one(
            "SELECT * FROM ocorrencias WHERE id = ?", (ocorrencia_id,)
        )
        if r is None:
            return jsonify({"erro": "Ocorrência não encontrada"}), 404
        item = dict(r)
        item["fotografia"] = (
            url_for("static", filename="uploads/" + r["fotografia"])
            if r["fotografia"]
            else None
        )
        item["cor"] = COR_NIVEIS.get(r["nivel_acumulo"], "#64748b")
        return jsonify(item)

    @app.route("/api/ocorrencias", methods=["POST"])
    def criar_ocorrencia():
        dados = request.form
        try:
            latitude = float(dados.get("latitude"))
            longitude = float(dados.get("longitude"))
        except (TypeError, ValueError):
            return jsonify({"erro": "Coordenadas inválidas."}), 400

        if not (-90.0 <= latitude <= 90.0) or not (-180.0 <= longitude <= 180.0):
            return jsonify({"erro": "Coordenadas fora do intervalo válido."}), 400

        tipo = dados.get("tipo_residuo", "").strip()
        nivel = dados.get("nivel_acumulo", "").strip()

        if tipo not in TIPOS_RESIDUO:
            return jsonify({"erro": "Tipo de resíduo inválido."}), 400
        if nivel not in NIVEIS_ACUMULO:
            return jsonify({"erro": "Nível de acúmulo inválido."}), 400

        fotografia_nome = None
        if "fotografia" in request.files:
            arquivo = request.files["fotografia"]
            if arquivo and arquivo.filename:
                if not _extensao_permitida(arquivo.filename):
                    return jsonify({"erro": "Formato de imagem não permitido."}), 400
                extensao = arquivo.filename.rsplit(".", 1)[-1].lower()
                fotografia_nome = f"ocorr_{uuid.uuid4().hex}.{extensao}"
                arquivo.save(os.path.join(UPLOAD_FOLDER, fotografia_nome))

        novo_id = database.query_insert(
            """
            INSERT INTO ocorrencias
                (latitude, longitude, fotografia, tipo_residuo, nivel_acumulo, observacoes, local_nome)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (
                latitude,
                longitude,
                fotografia_nome,
                tipo,
                nivel,
                dados.get("observacoes", "").strip() or None,
                dados.get("local_nome", "").strip() or None,
            ),
        )

        return jsonify({"id": novo_id, "url": url_for("detalhe", ocorrencia_id=novo_id)}), 201

    @app.errorhandler(413)
    def arquivo_grande(e):
        return jsonify({"erro": "Arquivo muito grande. Máximo 10 MB."}), 413

    return app


def _extensao_permitida(nome_arquivo):
    return "." in nome_arquivo and nome_arquivo.rsplit(
        ".", 1
    )[1].lower() in ALLOWED_EXTENSIONS


app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
