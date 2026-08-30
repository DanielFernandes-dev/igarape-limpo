---
tags:
  - guia
  - usuário
tipo: procedimento
status: atual
---

# Utilização do Sistema

## Navegação pública

Sem autenticação é possível:

- consultar o mapa em `/`;
- aplicar filtros e pesquisar ocorrências;
- abrir detalhes de ocorrências e pontos;
- consultar o dashboard;
- exportar CSV e GeoJSON;
- abrir a tela de registro, sem enviar o formulário.

## Entrar no sistema

1. Acesse `/login`.
2. Informe e-mail e senha.
3. Envie o formulário.
4. Após autenticação, use a navegação para abrir o registro de ocorrência.

## Registrar uma ocorrência

1. Acesse `/nova` com uma sessão ativa.
2. Defina a localização por geolocalização, clique no mapa ou seleção de ponto.
3. Confirme latitude e longitude.
4. Escolha o tipo de resíduo.
5. Escolha o nível de acúmulo.
6. Informe o nome do local e observações, se necessário.
7. Adicione uma fotografia opcional.
8. Revise o preview e envie.

Formatos de imagem aceitos: PNG, JPG, JPEG, GIF e WebP. O limite total da requisição é 10 MiB.

> [!tip] Privacidade em campo
> Evite fotografar rostos, placas, documentos e outros dados pessoais. A aplicação ainda não remove metadados das imagens.

## Filtrar o mapa

Os filtros podem ser combinados:

- tipo de resíduo;
- nível de acúmulo;
- ponto monitorado;
- data inicial e final;
- busca em local e observações.

O filtro visual de “pontos críticos” seleciona ocorrências de nível `Alto`. Consulte [[Glossário]] para não confundir esse recorte com pontos recorrentes.

## Consultar um ponto

Abra um ponto pelo mapa ou pela lista. A página apresenta:

- coordenadas e descrição;
- mapa de referência;
- quantidade de ocorrências;
- distribuições por tipo e nível;
- indicador de recorrência;
- histórico associado.

## Usar o dashboard

O dashboard apresenta totais, períodos recentes, pontos ativos, recorrência, tipos mais frequentes, evolução temporal e ranking.

Os dados são calculados a partir do banco local. Dados seed não devem ser apresentados como resultado ambiental.

## Exportar dados

Na página inicial, os botões CSV e GeoJSON acompanham os filtros ativos. Também é possível exportar diretamente pelos endpoints descritos em [[API HTTP]].

## Alterar status

A interface de detalhe apresenta o controle de status para moderadores e administradores. Os valores possíveis estão em [[Glossário]].

## Falhas de rede

O banco e as páginas locais continuam acessíveis, mas estes recursos podem falhar sem internet:

- tiles do OpenStreetMap;
- Leaflet, MarkerCluster e Chart.js carregados por CDN;
- fontes externas;
- Overpass, Open-Meteo e Nominatim.
