from config import OPEN_METEO_ENDPOINT, TIMEZONE
from app.utils import http


def buscar_clima(lat, lon, timezone=None):
    timezone = timezone or TIMEZONE
    params = {
        "latitude": str(lat),
        "longitude": str(lon),
        "timezone": timezone,
        "current": (
            "temperature_2m,relative_humidity_2m,precipitation,rain,"
            "wind_speed_10m,weather_code"
        ),
        "hourly": "precipitation_probability,precipitation",
        "forecast_days": "2",
    }
    try:
        _, dados = http.get(OPEN_METEO_ENDPOINT, params=params)
    except http.HttpError:
        raise

    atual = dados.get("current", {})
    horario = dados.get("hourly", {})
    return {
        "atual": {
            "temperatura": atual.get("temperature_2m"),
            "umidade": atual.get("relative_humidity_2m"),
            "precipitacao": atual.get("precipitation"),
            "chuva": atual.get("rain"),
            "vento": atual.get("wind_speed_10m"),
            "codigo_meteorologico": atual.get("weather_code"),
        },
        "previsao": {
            "tempos": horario.get("time", []),
            "probabilidade": horario.get("precipitation_probability", []),
            "precipitacao": horario.get("precipitation", []),
        },
        "fuso": timezone,
    }
