import csv
import io


def to_csv(lines, separador=";"):
    saida = io.StringIO()
    if separador == ";":
        writer = csv.writer(saida, delimiter=";")
    else:
        writer = csv.writer(saida)
    writer.writerows(lines)
    return saida.getvalue()


def to_geojson(features):
    return {
        "type": "FeatureCollection",
        "features": features,
    }


def ocorrencias_para_geojson(ocorrencias):
    features = []
    for o in ocorrencias:
        properties = {
            "id": o["id"],
            "data_hora": o["data_hora"],
            "tipo_residuo": o["tipo_residuo"],
            "nivel_acumulo": o["nivel_acumulo"],
            "status": o["status"],
            "local_nome": o["local_nome"] or "",
            "observacoes": o["observacoes"] or "",
        }
        if o.get("ponto_id"):
            properties["ponto_id"] = o["ponto_id"]
        features.append(
            {
                "type": "Feature",
                "geometry": {
                    "type": "Point",
                    "coordinates": [o["longitude"], o["latitude"]],
                },
                "properties": properties,
            }
        )
    return features


def ocorrencias_para_linhas(ocorrencias):
    cabecalho = [
        "id",
        "data_hora",
        "latitude",
        "longitude",
        "tipo_residuo",
        "nivel_acumulo",
        "status",
        "local_nome",
        "observacoes",
        "ponto_id",
    ]
    linhas = [cabecalho]
    for o in ocorrencias:
        linhas.append(
            [
                o["id"],
                o["data_hora"],
                o["latitude"],
                o["longitude"],
                o["tipo_residuo"],
                o["nivel_acumulo"],
                o["status"],
                o["local_nome"] or "",
                o["observacoes"] or "",
                o.get("ponto_id") or "",
            ]
        )
    return linhas


def sensores_para_linhas(stations):
    cabecalho = [
        "id",
        "name",
        "lat",
        "lon",
        "ph",
        "turbidity_ntu",
        "water_temperature_c",
        "dissolved_oxygen_mg_l",
        "conductivity_us_cm",
        "updated_at",
    ]
    linhas = [cabecalho]
    for s in stations:
        linhas.append(
            [
                s.get("id", ""),
                s.get("name", ""),
                s.get("lat", ""),
                s.get("lon", ""),
                s.get("ph", ""),
                s.get("turbidity_ntu", ""),
                s.get("water_temperature_c", ""),
                s.get("dissolved_oxygen_mg_l", ""),
                s.get("conductivity_us_cm", ""),
                s.get("updated_at", ""),
            ]
        )
    return linhas
