---
aliases:
  - Relatório Igarapé Limpo
tags:
  - relatório
  - igarape-limpo
tipo: relatório
status: rascunho
---

# IGARAPÉ LIMPO: SISTEMA COLABORATIVO PARA MONITORAMENTO DE RESÍDUOS SÓLIDOS EM CORPOS D'ÁGUA URBANOS

Autor: Daniel Fernandes de Oliveira e equipe

Orientador: ______

Centro Universitário de Ensino Superior

22/09/2026

## RESUMO

O presente relatório apresenta o estado de desenvolvimento do projeto Igarapé Limpo, sistema colaborativo destinado a registrar, localizar, acompanhar e analisar ocorrências de resíduos sólidos em corpos d'água urbanos. O sistema foi desenvolvido com backend em Python/Flask, banco de dados SQLite e frontend em HTML, CSS e JavaScript, com mapa interativo Leaflet e painel de indicadores Chart.js. O relatório descreve a metodologia adotada, a arquitetura em camadas, os recursos de segurança, a suíte de testes automatizados e as etapas já concluídas do planejamento. Ao final, são apresentadas as pendências do backlog, que compreendem a execução da pesquisa de campo com coleta de fotografias em igarapés e a fundamentação das funcionalidades com base em artigos científicos.

**Palavras-chave:** Igarapés. Resíduos sólidos. Monitoramento ambiental. Sistemas colaborativos. Geotecnologias.

## 1 Introdução

O descarte irregular de resíduos sólidos em igarapés urbanos é um problema ambiental e de saúde pública recorrente. Fotografias, coordenadas e observações isoladas dificultam a comparação de um mesmo local ao longo do tempo, dificultando o diagnóstico e o acompanhamento das áreas afetadas. Diante desse cenário, o projeto Igarapé Limpo propõe um sistema colaborativo que organiza essas observações como dados georreferenciados e históricos, oferecendo uma ferramenta de apoio para estudantes, pesquisadores, projetos de extensão, grupos ambientais e comunidades.

O desenvolvimento do projeto é gerenciado por meio de um quadro no Trello, que registra as atividades planejadas e o progresso de cada etapa. O quadro resume, em termos gerais, tudo o que já foi realizado no projeto; as únicas atividades ainda não concluídas são a pesquisa de campo, que prevê visitas a igarapés para coleta de fotografias de ambientes reais, a fundamentação das funcionalidades com artigos científicos e a elaboração do presente relatório.

![Figura 1 — Quadro de gestão do projeto no Trello. Fonte: produção própria.](docs/obsidian/07%20-%20Relatório/trello.jpeg)

Figura 1 — Quadro de gestão do projeto no Trello. Fonte: produção própria.

## 2 O que já foi feito

O plano de desenvolvimento do projeto foi organizado em fases, todas concluídas na sua totalidade. As entregas de cada etapa são descritas a seguir.

### 2.1 Fundamentos (MVP)

- Definição do escopo: nome do projeto, objetivo geral, objetivos específicos, público-alvo, tipos de resíduos, níveis de acúmulo e dados a serem armazenados.
- Backend Flask com API CRUD de ocorrências e upload de fotografias.
- Banco SQLite com tabelas de usuários, pontos monitorados e ocorrências, incluindo dados seed de teste.
- Frontend com páginas renderizadas via Jinja e integração do mapa Leaflet.
- Registro de ocorrência com geolocalização, seleção manual no mapa ou ponto monitorado.

### 2.2 Monitoramento e mapa

- Página de ponto monitorado com resumo, distribuições, recorrência e histórico.
- Filtros combináveis por tipo, nível, ponto, período e texto.
- Agrupamento de marcadores com MarkerCluster e diferenciação visual por nível de acúmulo.
- Exibição de ocorrências de nível alto (criticidade) e centralização no ponto selecionado.
- Lista recente e exportações sincronizadas com o recorte de filtros do mapa.

### 2.3 Gestão

- Autenticação com login, logout e sessão autenticada.
- Perfis de usuário: `usuario`, `moderador` e `administrador`.
- Status de ocorrência: `Nova`, `Em analise`, `Em atendimento`, `Resolvida` e `Descartada`.
- CRUD de ocorrências e gestão de pontos monitorados conforme permissão.

### 2.4 Dados e exportação

- Dashboard com totais gerais, ocorrências nos últimos 7 e 30 dias, pontos ativos e recorrentes.
- Gráficos por tipo, nível, evolução temporal e ranking de pontos.
- Exportação em CSV e GeoJSON, inclusive com os filtros aplicados.

### 2.5 Qualidade e segurança

- Senhas armazenadas com hash do Werkzeug.
- Cookies `HttpOnly`, `SameSite=Lax` e `Secure` por ambiente.
- Cabeçalhos HTTP de segurança (`X-Content-Type-Options`, `X-Frame-Options` e `Referrer-Policy`).
- Validação de coordenadas, domínios, tamanhos de campos e conteúdo real de imagens com Pillow.
- Limite de 10 MB por requisição.
- Respostas públicas sem `senha_hash` ou `usuario_id`.
- Logs de autenticação e operações sem dados sensíveis.
- Suíte com 20 testes automatizados aprovados, com banco e uploads temporários.

### 2.6 Interface e documentação

- Identidade visual temática com paleta de floresta, água, argila e areia.
- Layouts responsivos para desktop, tablet e celular.
- Acessibilidade com skip link, foco visível, regiões ARIA e suporte a `prefers-reduced-motion`.
- Documentação técnica navegável no Obsidian e documentos `README`, `ARQUITETURA`, `APRESENTACAO` e `TODO`.

## 3 Materiais e Métodos

O sistema foi desenvolvido com backend em Python e Flask 3.1, banco de dados SQLite e frontend em HTML, CSS e JavaScript puro, utilizando Leaflet e OpenStreetMap para o mapa e Chart.js para os gráficos. A arquitetura é organizada em camadas — rotas, serviços, repositórios, integrações externas e utilitários — o que favorece a manutenção e a validação independente de cada componente.

A metodologia de desenvolvimento seguiu um plano incremental em etapas, com modelagem do banco, implementação do backend, construção do frontend e do mapa, e posterior evolução em fases de monitoramento, gestão, dados, qualidade e documentação. A verificação das entregas foi realizada por meio de testes automatizados e de registros de evolução documentados no histórico do projeto.

O sistema também integra adaptadores externos auxiliares: hidrografia via Overpass, meteorologia via Open-Meteo, geocodificação reversa via Nominatim e um gateway JSON de sensores com exportação em CSV.

## 4 Resultados e Discussão

Os resultados obtidos até o momento são de natureza técnica: o protótipo está funcional e permite registrar uma ocorrência, associá-la a um ponto monitorado, filtrar os registros, visualizá-los no mapa, acompanhar o histórico, analisar indicadores no dashboard e exportar os dados recortados. A suíte de testes automatizados valida páginas, autenticação, proteção de rotas, filtros, exportações, privacidade e segurança.

Cabe destacar que os registros atualmente presentes no banco são dados seed e de teste, e não resultados de uma coleta ambiental formal. Nenhum resultado ambiental pode ser afirmado antes da realização da pesquisa de campo prevista. Como limitações do protótipo, destacam-se o uso de SQLite e armazenamento local de imagens, que não atendem alta concorrência; a ausência de migrações versionadas, recuperação de senha e proteção CSRF dedicada; e o fato de um usuário autenticado ainda poder atualizar ocorrências que não criou. A implantação em produção também não foi realizada, pois o projeto ainda depende das atividades de campo.

## 5 O que ainda falta

O backup do projeto registra atividades que permanecem pendentes e devem ser encerradas em conjunto:

- **Pesquisa de campo:** definição da área inicial de monitoramento, validação da metodologia e dos critérios de classificação, e execução de coletas controladas em igarapés.
- **Coleta de fotografias:** visita aos igarapés para registrar fotografias de ambientes reais e gerar casos de uso autênticos para o sistema.
- **Fundamentação científica:** coleta e estudo de artigos científicos para fundamentar e validar as funcionalidades já existentes do projeto.
- **Testes em campo:** verificação de precisão de localização, qualidade das fotografias, comportamento em dispositivos e conexões reais e revisão de usabilidade.
- **Elaboração do relatório:** o presente relatório acompanha a coleta e será complementado com os artigos e as fotografias obtidos, encerrando o backlog.

## 6 Considerações Finais

O projeto Igarapé Limpo encontra-se em estágio avançado de desenvolvimento, com todas as fases de implementação concluídas e validadas tecnicamente. O que permanece em aberto concentra-se na dimensão de campo e científica: a coleta de fotografias e dados reais em igarapés e a fundamentação teórica das funcionalidades com artigos científicos. A conclusão dessas atividades, juntamente com a finalização deste relatório, encerra o backlog previsto no quadro de gestão.

## REFERÊNCIAS

\_\_\_\_\_

> [!note] Referências pendentes
> As referências em norma ABNT serão adicionadas após a coleta dos artigos científicos prevista na etapa de pesquisa de campo.