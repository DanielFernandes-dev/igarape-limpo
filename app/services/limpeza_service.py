import os
import uuid
import math
from datetime import datetime

from flask import g, url_for
from PIL import Image, UnidentifiedImageError

import config
from app.repositories import limpeza_repository, ponto_repository
from app.services.ocorrencia_service import ErroValidacao


def validar(dados, arquivo=None):
    ponto_id = dados.get("ponto_id")
    try:
        ponto_id = int(ponto_id)
    except (TypeError, ValueError):
        raise ErroValidacao("Ponto monitorado inválido.")
    if ponto_repository.obter_por_id(ponto_id) is None:
        raise ErroValidacao("Ponto monitorado não encontrado.")

    data_hora = (dados.get("data_hora") or "").strip()
    try:
        data_hora = datetime.fromisoformat(data_hora).strftime("%Y-%m-%d %H:%M:%S")
    except (TypeError, ValueError):
        raise ErroValidacao("Data e horário da limpeza inválidos.")

    equipe = (dados.get("equipe") or "").strip()
    unidade = (dados.get("unidade") or "").strip()
    observacoes = (dados.get("observacoes") or "").strip()
    quantidade = dados.get("quantidade")
    try:
        quantidade = float(quantidade) if quantidade not in (None, "") else None
    except (TypeError, ValueError):
        raise ErroValidacao("Quantidade inválida.")
    if quantidade is not None and (
        not math.isfinite(quantidade) or quantidade < 0 or quantidade > 1_000_000
    ):
        raise ErroValidacao("Quantidade inválida.")
    if len(equipe) > 160 or len(unidade) > 30 or len(observacoes) > 2000:
        raise ErroValidacao("Dados da limpeza excedem o limite permitido.")
    if quantidade is not None and not unidade:
        raise ErroValidacao("Informe a unidade de medida da quantidade.")

    usuario = getattr(g, "current_user", None)
    return {
        "ponto_id": ponto_id,
        "data_hora": data_hora,
        "equipe": equipe or None,
        "quantidade": quantidade,
        "unidade": unidade or None,
        "observacoes": observacoes or None,
        "fotografia": salvar_fotografia(arquivo),
        "usuario_id": usuario["id"] if usuario else None,
    }


def criar(dados, arquivo=None):
    return limpeza_repository.criar(validar(dados, arquivo))


def salvar_fotografia(arquivo):
    if arquivo is None or not arquivo.filename:
        return None
    extensao = arquivo.filename.rsplit(".", 1)[-1].lower() if "." in arquivo.filename else ""
    if extensao not in config.ALLOWED_EXTENSIONS:
        raise ErroValidacao("Formato de imagem não permitido.")
    try:
        imagem = Image.open(arquivo.stream)
        formato = (imagem.format or "").lower()
        imagem.verify()
    except (UnidentifiedImageError, OSError, ValueError):
        raise ErroValidacao("O conteúdo do arquivo não corresponde a uma imagem permitida.")
    extensoes = {"jpeg": {"jpg", "jpeg"}, "png": {"png"}, "gif": {"gif"}, "webp": {"webp"}}
    if formato not in extensoes or extensao not in extensoes[formato]:
        raise ErroValidacao("O conteúdo do arquivo não corresponde à extensão informada.")
    arquivo.stream.seek(0)
    nome = f"limpeza_{uuid.uuid4().hex}.{extensao}"
    arquivo.save(os.path.join(config.UPLOAD_FOLDER, nome))
    return nome


def listar_por_ponto(ponto_id):
    itens = []
    for linha in limpeza_repository.listar_por_ponto(ponto_id):
        item = dict(linha)
        item.pop("usuario_id", None)
        item["fotografia"] = (
            url_for("static", filename="uploads/" + item["fotografia"])
            if item.get("fotografia") else None
        )
        itens.append(item)
    return itens
