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

Integrantes: Daniel Fernandes de Oliveira da Silva, Adriano Alves Barros, Carlos Johnatan Silva Souza Rodrigues e Julio Thiago Colares de Lima

Orientador: ______

Centro Universitário de Ensino Superior

22/09/2026

## RESUMO

O presente relatório apresenta o estado de desenvolvimento do projeto Igarapé Limpo, sistema colaborativo destinado a registrar, localizar, acompanhar e analisar ocorrências de resíduos sólidos em corpos d'água urbanos. O sistema foi desenvolvido com backend em Python/Flask, banco de dados SQLite e frontend em HTML, CSS e JavaScript, com mapa interativo Leaflet e painel de indicadores Chart.js. O relatório descreve a metodologia adotada, a arquitetura em camadas, os recursos de segurança, a suíte de testes automatizados, a fundamentação da problemática a partir de fontes sobre a situação dos igarapés urbanos de Manaus e as etapas já concluídas do planejamento. Ao final, são apresentadas as pendências do backlog, que compreendem a execução da pesquisa de campo com coleta de fotografias em igarapés e a conclusão da fundamentação das funcionalidades com base em artigos científicos.

**Palavras-chave:** Igarapés. Resíduos sólidos. Monitoramento ambiental. Sistemas colaborativos. Geotecnologias.

## 1 Introdução

O descarte irregular de resíduos sólidos em igarapés urbanos é um problema ambiental e de saúde pública recorrente. Fotografias, coordenadas e observações isoladas dificultam a comparação de um mesmo local ao longo do tempo, dificultando o diagnóstico e o acompanhamento das áreas afetadas. Diante desse cenário, o projeto Igarapé Limpo propõe um sistema colaborativo que organiza essas observações como dados georreferenciados e históricos, oferecendo uma ferramenta de apoio para estudantes, pesquisadores, projetos de extensão, grupos ambientais e comunidades.

O problema é amplamente documentado no contexto real de Manaus. Dos cerca de 150 igarapés em áreas urbanas da capital amazonense, a maioria sofre com poluição grave, esgoto sem tratamento e acúmulo de resíduos sólidos; mais de 80% dos cursos d'água da zona urbana apresentam algum tipo de comprometimento ambiental, e o descarte irregular de lixo transforma muitos trechos em canais de detritos. Pesquisas recentes apontam altos índices de microplásticos e esgoto não tratado em bacias urbanas importantes, como o Igarapé do Mindu e o Quarenta, e a contaminação eleva alertas de saúde pública, incluindo o risco de transmissão de malária em áreas vulneráveis. Esse cenário evidencia a pertinência de um sistema colaborativo que registre, localize e acompanhe ocorrências de resíduos nesses corpos d'água. A seção 3 apresenta a fundamentação que relaciona esse contexto às funcionalidades implementadas.

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

## 3 Fundamentação

Esta seção fundamenta o problema e valida as funcionalidades já existentes do projeto a partir de informações recentes sobre a situação dos igarapés urbanos de Manaus, coletadas em fontes jornalísticas e institucionais.

### 3.1 Situação atual dos igarapés urbanos de Manaus

A cidade de Manaus é cortada por cerca de mil igarapés, organizados em quatro grandes bacias urbanas: Educandos, São Raimundo, Puraquequara e Tarumã-Açu. Do grupo que corta a zona urbana — aproximadamente 150 igarapés — a maioria encontra-se em situação crítica: poluição grave, esgoto sem tratamento e acúmulo de resíduos sólidos, tendo perdido usos históricos como banho, lazer e navegação. O descarte irregular transforma muitos trechos em canais de detritos.

A contaminação é agravada pela falta de saneamento. Estudos apontam que apenas cerca de 22% do esgoto gerado em Manaus é tratado, colocando a capital entre os municípios com piores índices de saneamento entre as cidades mais populosas do país. O esgoto não tratado e o lixo descartado de forma irregular chegam diretamente aos corpos d'água, e pesquisas detectam microplásticos em bacias urbanas importantes, como o Igarapé do Mindu e o Quarenta. Em contraste, o Igarapé Água Branca é considerado um dos últimos trechos urbanos em estado mais preservado.

A poluição também se manifesta em riscos à saúde pública. Em ambientes contaminados, proliferam doenças como diarreia, leptospirose e dengue. A presença de criadouros naturais em balneários e margens de igarapés, por sua vez, eleva o risco de transmissão da malária em áreas vulneráveis: a cidade registrou 4.748 casos entre janeiro e agosto de 2026, com focos de infecção concentrados em localidades próximas a rios, igarapés e áreas de mata.

O quadro se agrava no período de estiagem. Com a descida do nível do Rio Negro, grandes volumes de lixo acumulado nas margens e nos leitos ficam expostos [1], o que motiva frentes de limpeza emergencial e ações de dragagem, como a que retirou cerca de 900 metros cúbicos de lixo e sedimentos no igarapé do Tarumã-Açu. O acúmulo de resíduos compromete ainda a drenagem das águas, elevando o risco de alagamentos durante fortes chuvas.

Como resposta parcial a esse cenário, a prefeitura utiliza tecnologias como as ecobarreiras em pontos específicos, como no Passeio do Mindu, para reter parte dos resíduos sólidos antes que cheguem aos rios principais.

![Figura 2 — Registro fotográfico de igarapé urbano de Manaus. Fonte: produção própria.](docs/obsidian/07%20-%20Relatório/igarape1.jpeg)

Figura 2 — Registro fotográfico de igarapé urbano de Manaus. Fonte: produção própria.

### 3.2 Validação das funcionalidades existentes

As informações apresentadas fundamentam diretamente as decisões de escopo e as funcionalidades já implementadas:

- **Registro georreferenciado de ocorrências**: a necessidade de registrar o descarte irregular com tipo de resíduo, nível de acúmulo, data e coordenadas é coerente com o problema descrito. Os tipos adotados (`Plastico`, `Metal`, `Vidro`, `Organico`, `Papel`, `Misto` e `Outro`) abrangem os resíduos citados nas fontes, como garrafas plásticas e embalagens.
- **Pontos monitorados**: o seed do banco cadastra o Igarapé do Mindu e o Igarapé do Educandos, que são, respectivamente, os principais contribuintes das bacias do São Raimundo e do Educandos. Isso confere coerência geográfica ao recorte inicial, ainda que a área de monitoramento oficial seja definida na pesquisa de campo.
- **Níveis de acúmulo e criticidade**: a escala `Baixo`, `Medio` e `Alto` e o filtro de criticidade (nível `Alto`) permitem priorizar os trechos que se tornam canais de detritos ou que acumulam lixo exposto na estiagem, apoiando o direcionamento de ações de limpeza e dragagem.
- **Recorrência e histórico**: o conceito de ponto recorrente (três ou mais ocorrências) e o histórico por ponto respondem à dinâmica real de reincidência do descarte, documentada pela necessidade de operações contínuas da Semulsp e da Seminf.
- **Fotografia e observações**: a documentação visual das ocorrências apoia o registro de evidências da poluição por esgoto e microplásticos e permite acompanhar a evolução de um mesmo trecho ao longo do tempo.
- **Dashboard e exportação**: os indicadores e as exportações em CSV e GeoJSON fornecem subsídios para análises semelhantes às realizadas em pesquisas citadas sobre contaminação e saneamento.

![Figura 3 — Registro fotográfico de acúmulo de resíduos em igarapé urbano. Fonte: produção própria.](docs/obsidian/07%20-%20Relatório/igarape2.jpeg)

Figura 3 — Registro fotográfico de acúmulo de resíduos em igarapé urbano. Fonte: produção própria.

### 3.3 Implicações para a pesquisa de campo

As fontes também orientam a pesquisa de campo prevista na seção 6: a área inicial de monitoramento deve considerar as bacias mencionadas (Mindu e Educandos) e os riscos à saúde associados, e a coleta deve prever o registro de trechos em período de estiagem, quando o acúmulo fica mais exposto. A comparação de ocorrências antes e depois das operações de limpeza e das ecobarreiras pode ainda fundamentar análises de efetividade no dashboard.

## 4 Materiais e Métodos

O sistema foi desenvolvido com backend em Python e Flask 3.1, banco de dados SQLite e frontend em HTML, CSS e JavaScript puro, utilizando Leaflet e OpenStreetMap para o mapa e Chart.js para os gráficos. A arquitetura é organizada em camadas — rotas, serviços, repositórios, integrações externas e utilitários — o que favorece a manutenção e a validação independente de cada componente.

A metodologia de desenvolvimento seguiu um plano incremental em etapas, com modelagem do banco, implementação do backend, construção do frontend e do mapa, e posterior evolução em fases de monitoramento, gestão, dados, qualidade e documentação. A verificação das entregas foi realizada por meio de testes automatizados e de registros de evolução documentados no histórico do projeto.

O sistema também integra adaptadores externos auxiliares: hidrografia via Overpass, meteorologia via Open-Meteo, geocodificação reversa via Nominatim e um gateway JSON de sensores com exportação em CSV.

## 5 Resultados e Discussão

Os resultados obtidos até o momento são de natureza técnica: o protótipo está funcional e permite registrar uma ocorrência, associá-la a um ponto monitorado, filtrar os registros, visualizá-los no mapa, acompanhar o histórico, analisar indicadores no dashboard e exportar os dados recortados. A suíte de testes automatizados valida páginas, autenticação, proteção de rotas, filtros, exportações, privacidade e segurança.

Cabe destacar que os registros atualmente presentes no banco são dados seed e de teste, e não resultados de uma coleta ambiental formal. Nenhum resultado ambiental pode ser afirmado antes da realização da pesquisa de campo prevista. Como limitações do protótipo, destacam-se o uso de SQLite e armazenamento local de imagens, que não atendem alta concorrência; a ausência de migrações versionadas, recuperação de senha e proteção CSRF dedicada; e o fato de um usuário autenticado ainda poder atualizar ocorrências que não criou. A implantação em produção também não foi realizada, pois o projeto ainda depende das atividades de campo.

## 6 O que ainda falta

O backup do projeto registra atividades que permanecem pendentes e devem ser encerradas em conjunto:

- **Pesquisa de campo:** definição da área inicial de monitoramento, validação da metodologia e dos critérios de classificação, e execução de coletas controladas em igarapés.
- **Coleta de fotografias:** visita aos igarapés para registrar fotografias de ambientes reais e gerar casos de uso autênticos para o sistema.
- **Fundamentação científica:** coleta e estudo de artigos científicos para fundamentar e validar as funcionalidades já existentes do projeto. Uma primeira etapa desta atividade foi concluída com a incorporação, na seção 3, de fontes sobre a situação dos igarapés urbanos de Manaus; novas fontes poderão ser acrescentadas conforme a pesquisa avance.
- **Testes em campo:** verificação de precisão de localização, qualidade das fotografias, comportamento em dispositivos e conexões reais e revisão de usabilidade.
- **Elaboração do relatório:** o presente relatório acompanha a coleta e será complementado com os artigos e as fotografias obtidos, encerrando o backlog.

## 7 Considerações Finais

O projeto Igarapé Limpo encontra-se em estágio avançado de desenvolvimento, com todas as fases de implementação concluídas e validadas tecnicamente. A fundamentação documental iniciada na seção 3 confirma a pertinência do recorte geográfico e das funcionalidades diante da situação real dos igarapés urbanos de Manaus. O que permanece em aberto concentra-se na dimensão de campo: a coleta de fotografias e dados reais em igarapés e a conclusão da fundamentação teórica das funcionalidades com novas fontes. A conclusão dessas atividades, juntamente com a finalização deste relatório, encerra o backlog previsto no quadro de gestão.

## REFERÊNCIAS

1. ALMEIDA FILHO, Paulo. **Os igarapés que cortam Manaus**. Manaus: Associação Comercial do Amazonas, 18 abr. 2023. Disponível em: https://aca.org.br/os-igarapes-que-cortam-manaus/. Acesso em: 22 set. 2026.

2. SOUZA, Almir. **Os igarapés esquecidos de Manaus**. Manaus: Olhar do Norte Brasil, 20 mar. 2026. Disponível em: https://www.olhardonortebrasil.com.br/os-igarapes-esquecidos-de-manaus/. Acesso em: 22 set. 2026.

3. MOTA E SILVA, Tiago da. **Dos igarapés aos manguezais, microplásticos contaminam a Amazônia**. Mongabay Brasil, 26 jun. 2026. Disponível em: https://brasil.mongabay.com/2026/06/dos-igarapes-aos-manguezais-microplasticos-contaminam-a-amazonia/. Acesso em: 22 set. 2026.

4. MANAUS. Prefeitura Municipal. Secretaria Municipal de Saúde. **Prefeitura de Manaus reforça alerta sobre risco de transmissão de malária em balneários e locais favoráveis aos criadouros naturais do mosquito Anopheles**. Manaus, 14 set. 2026. Disponível em: https://www.manaus.am.gov.br/semsa/alerta-risco-transmissao-malaria/. Acesso em: 22 set. 2026.

5. VLAXIO, Elanny. **As ecobarreiras podem salvar os igarapés de Manaus?** Amazônia Latitude, 19 jun. 2024. Disponível em: https://www.amazonialatitude.com/2024/06/19/ecobarreiras-podem-salvar-igarapes-manaus/. Acesso em: 22 set. 2026.

6. MANAUS REFORÇA orientações da Semsa sobre prevenção da malária em balneários e comunidades. **Portal Informe Manaus**, Manaus, 14 set. 2026. Disponível em: https://informemanaus.com.br/manaus-reforca-orientacoes-da-semsa-sobre-prevencao-da-malaria-em-balnearios-e-comunidades/09/. Acesso em: 22 set. 2026.

7. MANAUS. Prefeitura Municipal. Secretaria Municipal de Infraestrutura. **Prefeitura de Manaus retira 900 metros cúbicos de lixo de igarapé durante obra de dragagem e recupera fluxo das águas no Tarumã-Açu**. Manaus, 7 ago. 2026. Disponível em: https://www.manaus.am.gov.br/noticia/servicos/retira-lixo-igarape/. Acesso em: 22 set. 2026.
