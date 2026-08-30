from app.utils import http


def buscar_local(lat, lon, idioma="pt-BR"):
    params = {
        "format": "jsonv2",
        "lat": str(lat),
        "lon": str(lon),
        "zoom": "14",
        "addressdetails": "1",
        "accept-language": idioma,
    }
    try:
        _, dados = http.get("https://nominatim.openstreetmap.org/reverse", params=params, timeout=10)
    except http.HttpError:
        raise

    endereco = dados.get("address", {}) or {}
    nome = (
        endereco.get("suburb")
        or endereco.get("neighbourhood")
        or endereco.get("city_district")
        or endereco.get("city")
        or dados.get("display_name")
        or "Localização atual"
    )
    return {
        "rotulo": nome,
        "display_name": dados.get("display_name"),
        "bairro": endereco.get("suburb")
        or endereco.get("neighbourhood")
        or endereco.get("city_district"),
        "cidade": endereco.get("city"),
        "regiao": endereco.get("state"),
    }
