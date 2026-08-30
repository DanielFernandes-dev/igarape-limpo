from app.integrations import nominatim, openmeteo, overpass, sensor_gateway
from app.utils import http


def status_integracoes(bbox=None):
    """
    Retorna o estado de cada integração sem fazer chamadas pesadas:
    apenas um teste curto de conectividade quando possível.
    Para o gateway, retorna 'não configurado' de forma conservadora.
    """
    resultados = {}

    resultados["hidrografia"] = _estado_hidrografia()
    resultados["meteorologia"] = _estado_meteorologia()
    resultados["geocodificacao"] = _estado_geocodificacao()
    resultados["sensores"] = {
        "rotulo": "Sensores (gateway)",
        "estado": "nao_configurado",
        "detalhe": "Configuração fornecida pelo navegador sob demanda",
    }
    return resultados


def _estado_hidrografia():
    from config import BOUNDING_BOX, OVER_PASS_ENDPOINTS

    try:
        resultado = overpass.buscar_hidrografia(BOUNDING_BOX, trechos_maximo=5)
        return {
            "rotulo": "Hidrografia (Overpass)",
            "estado": "ativo",
            "detalhe": f"{len(resultado['trechos'])} trechos encontrados",
            "endpoints": OVER_PASS_ENDPOINTS,
        }
    except http.HttpError as exc:
        return {
            "rotulo": "Hidrografia (Overpass)",
            "estado": "erro",
            "detalhe": exc.message,
            "endpoints": OVER_PASS_ENDPOINTS,
        }


def _estado_meteorologia():
    from config import MANAUS

    try:
        openmeteo.buscar_clima(MANAUS["lat"], MANAUS["lon"])
        return {
            "rotulo": "Meteorologia (Open-Meteo)",
            "estado": "ativo",
            "detalhe": "Previsão obtida",
        }
    except http.HttpError as exc:
        return {
            "rotulo": "Meteorologia (Open-Meteo)",
            "estado": "erro",
            "detalhe": exc.message,
        }


def _estado_geocodificacao():
    from config import MANAUS

    try:
        nominatim.buscar_local(MANAUS["lat"], MANAUS["lon"])
        return {
            "rotulo": "Geocodificação (Nominatim)",
            "estado": "ativo",
            "detalhe": "Busca disponível",
        }
    except http.HttpError as exc:
        return {
            "rotulo": "Geocodificação (Nominatim)",
            "estado": "erro",
            "detalhe": exc.message,
        }
