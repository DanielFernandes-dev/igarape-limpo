import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

DATABASE_PATH = os.path.join(BASE_DIR, "igarape_vivo.db")
SCHEMA_PATH = os.path.join(BASE_DIR, "schema.sql")

UPLOAD_FOLDER = os.path.join(BASE_DIR, "static", "uploads")
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif", "webp"}
MAX_CONTENT_LENGTH = 10 * 1024 * 1024

TIPOS_RESIDUO = ["Plastico", "Metal", "Vidro", "Organico", "Papel", "Misto", "Outro"]
NIVEIS_ACUMULO = ["Baixo", "Medio", "Alto"]

COR_NIVEIS = {
    "Baixo": "#22c55e",
    "Medio": "#eab308",
    "Alto": "#ef4444",
}
