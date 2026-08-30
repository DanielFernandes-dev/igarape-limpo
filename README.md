Igarapé Vivo

Sistema de monitoramento colaborativo de resíduos sólidos em corpos d'água urbanos.

Sobre o projeto

O Igarapé Vivo é um protótipo de aplicação voltado ao registro, georreferenciamento e acompanhamento de resíduos sólidos encontrados em igarapés e outros corpos d'água urbanos.

A proposta é utilizar tecnologia para transformar observações ambientais dispersas em dados organizados, permitindo visualizar onde existem ocorrências de resíduos, quais tipos são mais frequentes e como esses pontos evoluem ao longo do tempo.

O projeto não pretende substituir órgãos públicos, equipes de limpeza ou sistemas oficiais de monitoramento. Seu objetivo é desenvolver uma ferramenta tecnológica de apoio à observação e análise ambiental.

Problema

O descarte inadequado de resíduos sólidos em corpos d'água urbanos pode provocar acúmulo de lixo, obstrução do fluxo da água, degradação ambiental e contribuir para problemas urbanos como alagamentos.

Apesar da existência de estudos e ações de monitoramento, informações sobre ocorrências podem estar dispersas entre observações de campo, fotografias e diferentes fontes de dados.

O projeto propõe centralizar essas informações em uma plataforma simples e visual.

Objetivo

Desenvolver um protótipo capaz de:

- registrar ocorrências de resíduos;
- armazenar a localização geográfica da ocorrência;
- registrar fotografias;
- classificar o tipo de resíduo observado;
- estimar o nível de acúmulo;
- apresentar as ocorrências em um mapa;
- permitir consultar o histórico de um determinado ponto;
- gerar informações básicas para análise dos locais mais recorrentes;
- (evolução) filtrar e pesquisar ocorrências;
- (evolução) acompanhar pontos monitorados e status das ocorrências;
- (evolução) apresentar dashboard analítico com gráficos;
- (evolução) exportar os dados para análise externa.

Público-alvo

O protótipo poderá ser utilizado por:

- estudantes e pesquisadores;
- projetos de extensão;
- grupos ambientais;
- comunidades próximas a igarapés;
- voluntários em atividades de monitoramento;
- instituições interessadas em dados ambientais.

Funcionamento

O fluxo básico será:

Usuário
   ↓
Registra ocorrência
   ↓
Localização + fotografia + classificação
   ↓
Servidor
   ↓
Banco de dados
   ↓
Mapa, pontos monitorados e dashboard
   ↓
Análise, acompanhamento e exportação das ocorrências

Registro de ocorrência

Cada ocorrência poderá conter:

- latitude;
- longitude;
- data e horário;
- fotografia;
- tipo de resíduo;
- nível estimado de acúmulo;
- observações adicionais;
- (evolução) ponto monitorado associado;
- (evolução) status de acompanhamento (Nova, Em análise, Em atendimento, Resolvida, Descartada).

Exemplo:

Ocorrência #038

Local:
Igarapé do Mindu

Tipo:
Plástico

Acúmulo:
Alto

Data:
24/08/2026

Coordenadas:
-3.xxxxxx, -60.xxxxxx

Fotografia:
imagem.jpg

Mapa

As ocorrências serão apresentadas em um mapa.

Uma possível representação:

🟢 Baixo acúmulo
🟡 Médio acúmulo
🔴 Alto acúmulo

Ao selecionar um ponto, o usuário poderá visualizar as informações daquela ocorrência.

Na evolução, o mapa passa a ser o principal ambiente de exploração, com filtros combináveis (tipo de resíduo, nível, período, local), pesquisa, exibição de pontos críticos, centralização no ponto selecionado e agrupamento de marcadores quando houver muitos registros.

Histórico e ponto monitorado

Um dos diferenciais do projeto será o acompanhamento temporal.

Em vez de registrar apenas:

«"Existe lixo neste local."»

o sistema poderá armazenar várias observações:

01/09 → Acúmulo alto
15/09 → Acúmulo médio
30/09 → Acúmulo baixo
15/10 → Acúmulo alto

Isso permitirá identificar locais em que o acúmulo de resíduos é recorrente.

Na evolução, cada local será associado a um **ponto monitorado**, com página própria contendo histórico, distribuição por tipo e nível, recorrência, status e fotografias — permitindo comparar o estado do mesmo local ao longo do tempo.

Exemplo de interpretação:

«"Este ponto apresentou 12 ocorrências nos últimos 3 meses e registrou nível alto de acúmulo em 4 ocasiões."»

Dashboard

O protótipo poderá apresentar indicadores como:

- quantidade total de ocorrências;
- ocorrências nos últimos 7 e 30 dias;
- quantidade de ocorrências por tipo de resíduo;
- quantidade de ocorrências por região/ponto;
- pontos com maior recorrência;
- pontos críticos;
- evolução das ocorrências ao longo do tempo;
- ranking dos pontos e comparação entre períodos.

O MVP já exibe um resumo inicial (ocorrências registradas, pontos monitorados, maior ocorrência e pontos críticos). A evolução adiciona gráficos temporais e por categoria.

Exemplo:

OCORRÊNCIAS REGISTRADAS
128

PONTOS MONITORADOS
37

MAIOR OCORRÊNCIA
Plástico

PONTOS CRÍTICOS
8

Visão computacional

A classificação automática de resíduos por imagem será considerada uma etapa posterior.

A ideia é permitir que uma fotografia seja analisada por um modelo de visão computacional capaz de identificar a presença ou o tipo predominante de resíduos.

Exemplo:

Fotografia
    ↓
Modelo de visão computacional
    ↓
Resíduos detectados
    ↓
Classificação

Essa funcionalidade não faz parte do primeiro MVP. Primeiro será construída a infraestrutura de coleta e organização dos dados.

Escopo do MVP

A primeira versão deverá conter somente o necessário para validar a proposta:

1. cadastro de ocorrência;
2. obtenção ou inserção da localização;
3. envio de fotografia;
4. classificação manual do resíduo;
5. classificação do nível de acúmulo;
6. armazenamento no banco de dados;
7. visualização das ocorrências em mapa;
8. consulta das informações de uma ocorrência.

Funcionalidades como inteligência artificial, alertas automáticos e monitoramento por câmeras ficam para versões posteriores.

Status do MVP — implementado

O protótipo MVP está funcional e cobre o escopo acima:

- registro de ocorrência com localização (Geolocation API ou clique no mapa);
- upload de fotografia;
- classificação de tipo de resíduo e nível de acúmulo;
- persistência em SQLite;
- mapa Leaflet com marcadores coloridos por nível de acúmulo;
- página de detalhe de cada ocorrência;
- cards de resumo e lista de ocorrências recentes;
- API completa de CRUD (cadastrar, consultar, atualizar e excluir ocorrências);
- exportação dos dados em CSV;
- integrações auxiliares: hidrografia (Overpass), meteorologia (Open-Meteo), geocodificação (Nominatim) e gateway de sensores.

O backend é organizado em camadas dentro do pacote `app/` (rotas, serviços e repositórios), com `create_app()` em `app/__init__.py` e os blueprints de páginas (`app/routes/pages.py`) e de API (`app/routes/api.py`).

A evolução para o monitoramento (pontos, históricos, dashboard, filtros, gestão e exportação) está descrita nas versões V2 acima.

Tecnologias

Stack escolhida para o protótipo (MVP):

- Frontend: HTML, CSS e JavaScript puro;
- Backend: Python + Flask;
- Banco de dados: SQLite (SQL);
- Mapa: Leaflet (OpenStreetMap), sem chave de API;
- Armazenamento: SQLite para as informações e pasta local para as fotografias enviadas;
- Futuro: modelo de machine learning para análise das fotografias.

Evoluções tecnológicas previstas (V2+):

- clusterização de marcadores no mapa (plugin do Leaflet);
- filtros e pesquisa por API;
- dashboard analítico com gráficos;
- exportação em CSV e, posteriormente, GeoJSON;
- autenticação e perfis de usuário;
- possível migração para PostgreSQL com suporte espacial conforme a escala.

A arquitetura prioriza simplicidade e facilidade de manutenção. Detalhes completos estão no relatório de arquitetura (ARQUITETURA.md).

Como executar

Crie o ambiente virtual e instale as dependências:

    python3 -m venv .venv
    .venv/bin/pip install -r requirements.txt

Em seguida, inicie o servidor:

    .venv/bin/python app.py

Abra http://127.0.0.1:5000 no navegador.

O banco de dados (igarape_vivo.db) é criado e preenchido com dados de exemplo automaticamente na primeira execução. As fotografias enviadas são salvas em static/uploads/.

Evolução planejada

Versão 1 — MVP

Registro e visualização das ocorrências. *(implementado)*

Versão 2 — Monitoramento

Filtros, dashboard, pontos monitorados, histórico e identificação de recorrências.

Versão 2.1 — Gestão

Status das ocorrências, fluxo de acompanhamento, autenticação, perfis e permissões, além de melhoria na segurança dos arquivos.

Versão 2.2 — Dados

Exportação dos dados em CSV/GeoJSON e melhorias analíticas.

Versão 3 — Inteligência

Classificação automática de resíduos por imagem.

Versão 4 — Monitoramento automático

Sistema de alertas baseado no aumento de resíduos e, futuramente, possibilidade de integração com câmeras ou outros sensores.

Fluxo alvo da evolução

O projeto amplia o fluxo central do MVP:

> registrar → armazenar → localizar → visualizar

para:

> registrar → validar → localizar → visualizar → analisar → acompanhar → comparar → exportar

A principal evolução estrutural é a introdução do conceito de **ponto monitorado**, associado a um histórico de ocorrências, permitindo acompanhar a frequência, a recorrência e a evolução temporal de cada local.

ODS relacionados

O projeto pode contribuir principalmente para:

- ODS 9 — Indústria, Inovação e Infraestrutura
- ODS 11 — Cidades e Comunidades Sustentáveis
- ODS 12 — Consumo e Produção Responsáveis
- ODS 6 — Água Potável e Saneamento

A relação definitiva com os ODS deverá ser estabelecida de acordo com o objetivo e os resultados efetivamente obtidos no projeto.

Princípio do projeto

O Igarapé Vivo não pretende "resolver a poluição dos igarapés".

Seu objetivo é mais específico:

«Transformar observações sobre resíduos em dados georreferenciados que possam ser visualizados, comparados e acompanhados ao longo do tempo.»

Essa delimitação mantém o projeto tecnicamente viável e permite que novas funcionalidades sejam adicionadas posteriormente.
