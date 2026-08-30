---
tags:
  - integrações
  - serviços-externos
tipo: referência
status: atual
---

# Integrações Externas

## Visão geral

Os adaptadores ficam em `app/integrations/` e são chamados pelo backend. Isso evita problemas de CORS no navegador, mas faz o servidor assumir os riscos e limites das requisições externas.

## Overpass e OpenStreetMap

`overpass.py` consulta cursos d'água nomeados dentro do bounding box configurado para Manaus.

- possui dois endpoints de fallback;
- limita a quantidade de trechos retornados;
- depende da disponibilidade pública do Overpass.

Endpoint interno: `GET /api/integracao/hidrografia`.

## Open-Meteo

`openmeteo.py` consulta condições atuais e previsão de precipitação para coordenadas fornecidas.

Endpoint interno:

```http
GET /api/integracao/meteo?lat=-3.119&lon=-60.0217
```

## Nominatim

`nominatim.py` realiza geocodificação reversa.

Endpoint interno:

```http
GET /api/integracao/geocode?lat=-3.119&lon=-60.0217
```

O adaptador usa atualmente uma URL literal, embora exista `NOMINATIM_ENDPOINT` em `config.py`.

## Gateway de sensores

`sensor_gateway.py` consulta uma URL JSON e pode enviar um token Bearer. No protótipo, o cliente informa `url` e `token` ao endpoint.

```json
{
  "url": "https://gateway.example.org/dados",
  "token": "opcional"
}
```

Endpoints:

- `POST /api/integracao/sensores`;
- `POST /api/export/sensores.csv`.

> [!danger] Risco de SSRF
> Como a URL é fornecida pelo cliente e a rota é pública, o servidor pode ser induzido a acessar destinos indevidos. Antes de produção, a URL deve ser configurada no servidor e limitada por allowlist.

## Status das integrações

`GET /api/integracao/status` realiza chamadas reais a Overpass, Open-Meteo e Nominatim. Portanto, pode ser lento, consumir limites externos e falhar por indisponibilidade de terceiros.

## Tratamento de falhas

Falhas HTTP externas conhecidas retornam normalmente HTTP 502 na API interna. Isso não impede o acesso aos dados locais e às páginas renderizadas.

Coordenadas não numéricas podem provocar erro interno em rotas que executam `float()` sem capturar `ValueError`.

## Interface atual

As integrações possuem adaptadores e endpoints, mas não formam um painel visual completo. Nominatim e meteorologia não preenchem automaticamente o formulário de ocorrência.

## Dependências do frontend

Além das integrações do backend, o navegador acessa:

- tiles do OpenStreetMap;
- unpkg para Leaflet e MarkerCluster;
- jsDelivr para Chart.js;
- Google Fonts.

## Boas práticas operacionais

- definir timeouts e limites;
- respeitar políticas de uso dos provedores;
- identificar adequadamente requisições ao Nominatim;
- não expor tokens em logs ou respostas;
- adicionar cache onde permitido;
- monitorar indisponibilidade e limite de chamadas;
- restringir todos os destinos acessíveis pelo gateway.

Veja [[Segurança e Privacidade]] e [[Implantação]].
