from app.utils import http


def buscar_hidrografia(bbox, trechos_maximo=None, endpoints=None):
    """
    Consulta cursos d'água do OpenStreetMap dentro de um bounding box.

    bbox: tupla (sul, oeste, norte, leste).
    Retorna: lista de {nome, waterway, trecho: [[lat, lon], ...]}.
    """
    endpoints = endpoints or _endpoints()
    sul, oeste, norte, leste = bbox
    trechos_maximo = trechos_maximo or 200
    query = (
        '[out:json][timeout:25];\n'
        'way["waterway"~"river|stream|canal"]["name"]'
        f"({sul},{oeste},{norte},{leste});\n"
        "out tags geom;"
    )

    ultimo_erro = None
    for endpoint in endpoints:
        try:
            _, dados = http.post(endpoint, form={"data": query}, timeout=20)
            elementos = [
                e
                for e in dados.get("elements", [])
                if isinstance(e.get("geometry"), list) and e["geometry"]
            ][:trechos_maximo]

            trechos = []
            nomes = set()
            for el in elementos:
                pontos = [[p["lat"], p["lon"]] for p in el["geometry"]]
                nome = el.get("tags", {}).get("name") or "Curso d'água"
                nomes.add(nome)
                trechos.append(
                    {
                        "nome": nome,
                        "waterway": el.get("tags", {}).get("waterway", "waterway"),
                        "trecho": pontos,
                    }
                )
            return {"trechos": trechos, "nomes_unicos": list(nomes)}
        except http.HttpError as exc:
            ultimo_erro = exc

    raise http.HttpError(
        f"Hidrografia indisponível ({ultimo_erro.message if ultimo_erro else 'sem endpoint'})"
    )


def _endpoints():
    from config import OVER_PASS_ENDPOINTS

    return list(OVER_PASS_ENDPOINTS)
