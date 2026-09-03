import ipaddress
import socket
from urllib.parse import urlparse

from app.utils import http

CAMPOS_ESPERADOS = [
    "ph",
    "turbidity_ntu",
    "water_temperature_c",
    "dissolved_oxygen_mg_l",
    "conductivity_us_cm",
]


def conectar_gateway(url, token=None, timeout=15):
    """
    Busca a telemetria de estações de um gateway externo.

    Fonte e destino: a configuração (url + token) chega por parâmetro
    (originada no navegador), mas quem realiza a chamada externa é o
    backend, evitando CORS e exposição da chamada no navegador.
    """
    _validar_url_gateway(url)
    headers = {"Accept": "application/json"}
    if token:
        headers["Authorization"] = f"Bearer {token}"

    try:
        _, dados = http.get(url, headers=headers, timeout=timeout, params=None)
    except http.HttpError:
        raise

    stations = dados if isinstance(dados, list) else dados.get("stations", [])
    if not isinstance(stations, list):
        raise http.HttpError("Formato inválido: campo 'stations' ausente ou não é lista")

    estacoes = [
        _normalizar(s)
        for s in stations
        if isinstance(s, dict)
        and _flutuante(s.get("lat"))
        and _flutuante(s.get("lon"))
    ]
    return estacoes


def _validar_url_gateway(url):
    try:
        parsed = urlparse(url)
    except ValueError:
        raise http.HttpError("URL do gateway inválida.")
    if parsed.scheme not in ("http", "https") or not parsed.hostname:
        raise http.HttpError("URL do gateway inválida.")
    try:
        enderecos = socket.getaddrinfo(parsed.hostname, parsed.port, type=socket.SOCK_STREAM)
    except (OSError, ValueError):
        raise http.HttpError("Não foi possível resolver o gateway.")
    for endereco in {item[4][0] for item in enderecos}:
        ip = ipaddress.ip_address(endereco)
        if ip.is_private or ip.is_loopback or ip.is_link_local or ip.is_multicast or ip.is_unspecified:
            raise http.HttpError("O gateway não pode apontar para uma rede privada.")


def _normalizar(estacao):
    normalizada = {"id": estacao.get("id"), "name": estacao.get("name")}
    for campo in CAMPOS_ESPERADOS:
        normalizada[campo] = _flutuante(estacao.get(campo))
    normalizada["lat"] = _flutuante(estacao.get("lat"))
    normalizada["lon"] = _flutuante(estacao.get("lon"))
    normalizada["updated_at"] = estacao.get("updated_at")
    return normalizada


def _flutuante(valor):
    try:
        if valor is None or valor == "":
            return None
        return float(valor)
    except (TypeError, ValueError):
        return None
