import os
import secrets

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

SECRET_KEY = os.environ.get("IGARAPE_SECRET_KEY", secrets.token_hex(16))

DATABASE_PATH = os.path.join(BASE_DIR, "igarape_vivo.db")
SCHEMA_PATH = os.path.join(BASE_DIR, "schema.sql")

UPLOAD_FOLDER = os.path.join(BASE_DIR, "static", "uploads")
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif", "webp"}
MAX_CONTENT_LENGTH = 10 * 1024 * 1024

TIPOS_RESIDUO = ["Plastico", "Metal", "Vidro", "Organico", "Papel", "Misto", "Outro"]
NIVEIS_ACUMULO = ["Baixo", "Medio", "Alto"]

STATUS_OCORRENCIA = [
    "Nova",
    "Em analise",
    "Em atendimento",
    "Resolvida",
    "Descartada",
]
STATUS_PONTO = ["Ativo", "Inativo"]

COR_NIVEIS = {
    "Baixo": "#22c55e",
    "Medio": "#eab308",
    "Alto": "#ef4444",
}

MANAUS = {"lat": -3.1190, "lon": -60.0217, "zoom": 12}
TIMEZONE = "America/Manaus"

# Hidrografia (Overpass)
BOUNDING_BOX = (-3.23, -60.20, -2.95, -59.85)  # (sul, oeste, norte, leste)
OVER_PASS_ENDPOINTS = [
    "https://overpass-api.de/api/interpreter",
    "https://overpass.kumi.systems/api/interpreter",
]
MAX_HIDROGRAFIA_TRECHOS = 180

# Meteorologia (Open-Meteo)
OPEN_METEO_ENDPOINT = "https://api.open-meteo.com/v1/forecast"

# Geocodificação (Nominatim)
NOMINATIM_ENDPOINT = "https://nominatim.openstreetmap.org/reverse"
