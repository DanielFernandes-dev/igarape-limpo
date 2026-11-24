# CAPA

Daniel Fernandes de Oliveira da Silva

Adriano Alves Barros

Carlos Johnatan Silva Souza Rodrigues

Julio Thiago Colares de Lima

**IGARAPÉ LIMPO: SISTEMA COLABORATIVO PARA MONITORAMENTO DE RESÍDUOS SÓLIDOS EM CORPOS D'ÁGUA URBANOS**

Manaus, AM

22 de setembro de 2026

---

# FOLHA DE ROSTO

Daniel Fernandes de Oliveira da Silva

Adriano Alves Barros

Carlos Johnatan Silva Souza Rodrigues

Julio Thiago Colares de Lima

**IGARAPÉ LIMPO: SISTEMA COLABORATIVO PARA MONITORAMENTO DE RESÍDUOS SÓLIDOS EM CORPOS D'ÁGUA URBANOS**

Projeto de extensão apresentado ao CIESA. Relatório do desenvolvimento do sistema e planejamento das atividades com a comunidade externa.

Curso: a informar.

Período: a informar.

Orientador: a informar.

Manaus, AM

22 de setembro de 2026

---

<!-- Orientações para diagramação na exportação: papel A4; fonte Arial ou Times New Roman, tamanho 12; espaçamento 1,5 no corpo e simples na capa e folha de rosto. Contar as páginas a partir da folha de rosto, excluindo a capa. Seções primárias em caixa alta e negrito; secundárias em caixa alta sem negrito; terciárias em caixa baixa e negrito; quaternárias em caixa baixa sem negrito. O estilo dos títulos deve ser ajustado no exportador, pois depende do renderizador Markdown. Atualizar a paginação do sumário após a diagramação. -->

# SUMÁRIO

- [1 INTRODUÇÃO](#1-introdução)
  - [1.1 OBJETO SOCIAL FOCO DA ATIVIDADE DE EXTENSÃO](#11-objeto-social-foco-da-atividade-de-extensão)
  - [1.2 PROBLEMÁTICA SOCIAL](#12-problemática-social)
  - [1.3 MOTIVAÇÕES PARA A ATIVIDADE DE EXTENSÃO](#13-motivações-para-a-atividade-de-extensão)
  - [1.4 OBJETIVOS](#14-objetivos)
    - [1.4.1 Objetivo geral](#141-objetivo-geral)
    - [1.4.2 Objetivos específicos](#142-objetivos-específicos)
  - [1.5 JUSTIFICATIVA](#15-justificativa)
- [2 REFERENCIAL TEÓRICO](#2-referencial-teórico)
  - [2.1 CONTEXTO DOS IGARAPÉS URBANOS DE MANAUS](#21-contexto-dos-igarapés-urbanos-de-manaus)
  - [2.2 RELAÇÃO ENTRE O CONTEXTO AMBIENTAL E AS FUNCIONALIDADES](#22-relação-entre-o-contexto-ambiental-e-as-funcionalidades)
  - [2.3 IMPLICAÇÕES PARA A PESQUISA DE CAMPO](#23-implicações-para-a-pesquisa-de-campo)
- [3 METODOLOGIA](#3-metodologia)
  - [3.1 PROCEDIMENTOS E INSTRUMENTOS METODOLÓGICOS](#31-procedimentos-e-instrumentos-metodológicos)
    - [3.1.1 Público envolvido](#311-público-envolvido)
    - [3.1.2 Plano de trabalho, atividades vinculadas aos objetivos e etapas](#312-plano-de-trabalho-atividades-vinculadas-aos-objetivos-e-etapas)
    - [3.1.3 Cronograma das etapas do projeto](#313-cronograma-das-etapas-do-projeto)
  - [3.2 ACOMPANHAMENTO E AVALIAÇÃO](#32-acompanhamento-e-avaliação)
- [4 PROTAGONISMO DA COMUNIDADE EXTERNA](#4-protagonismo-da-comunidade-externa)
- [5 RELAÇÃO ENSINO, PESQUISA E EXTENSÃO](#5-relação-ensino-pesquisa-e-extensão)
- [6 RESULTADOS ESPERADOS](#6-resultados-esperados)
  - [6.1 ENTREGAS TÉCNICAS JÁ REALIZADAS](#61-entregas-técnicas-já-realizadas)
    - [6.1.1 Fundamentos (MVP)](#611-fundamentos-mvp)
    - [6.1.2 Monitoramento e mapa](#612-monitoramento-e-mapa)
    - [6.1.3 Gestão](#613-gestão)
    - [6.1.4 Dados e exportação](#614-dados-e-exportação)
    - [6.1.5 Qualidade e segurança](#615-qualidade-e-segurança)
    - [6.1.6 Interface e documentação](#616-interface-e-documentação)
  - [6.2 RESULTADOS ACADÊMICOS E SOCIAIS ESPERADOS](#62-resultados-acadêmicos-e-sociais-esperados)
- [7 LIMITAÇÕES DA ATIVIDADE DE EXTENSÃO](#7-limitações-da-atividade-de-extensão)
- [8 RECURSOS](#8-recursos)
- [REFERÊNCIAS](#referências)

## 1 INTRODUÇÃO

O descarte irregular de resíduos sólidos em igarapés urbanos é um problema ambiental e de saúde pública recorrente. Fotografias, coordenadas e observações isoladas dificultam a comparação de um mesmo local ao longo do tempo, dificultando o diagnóstico e o acompanhamento das áreas afetadas. Diante desse cenário, o projeto Igarapé Limpo propõe um sistema colaborativo que organiza essas observações como dados georreferenciados e históricos, oferecendo uma ferramenta de apoio para estudantes, pesquisadores, projetos de extensão, grupos ambientais e comunidades.

### 1.1 OBJETO SOCIAL FOCO DA ATIVIDADE DE EXTENSÃO

A atividade tem como foco o registro e o acompanhamento colaborativo do descarte irregular e do acúmulo de resíduos sólidos em igarapés urbanos de Manaus. Os dados de demonstração incluem referências ao Mindu, Educandos, Quarenta e Tarumã-Açu; não representam coleta ambiental real. Os trechos efetivos de atuação serão definidos e validados na etapa de campo com a comunidade externa.

### 1.2 PROBLEMÁTICA SOCIAL

O acúmulo de resíduos nos igarapés compromete a qualidade ambiental e a drenagem urbana. A dispersão de fotografias e relatos dificulta a identificação de locais com descarte recorrente e o acompanhamento dos mesmos trechos ao longo do tempo. O contexto documental apresentado na seção 2 evidencia a necessidade de organizar essas informações de forma acessível aos públicos envolvidos.

### 1.3 MOTIVAÇÕES PARA A ATIVIDADE DE EXTENSÃO

A proposta surgiu da possibilidade de aplicar conhecimentos de desenvolvimento de software a uma questão ambiental do território de Manaus. A equipe busca aproximar a formação acadêmica das necessidades de estudantes, grupos ambientais e moradores, por meio de uma ferramenta de registro e consulta de observações ambientais.

### 1.4 OBJETIVOS

#### 1.4.1 Objetivo geral

Apoiar o monitoramento colaborativo de resíduos sólidos em igarapés urbanos de Manaus por meio do sistema Igarapé Limpo.

Busca-se, assim, a organização de registros georreferenciados e históricos como subsídio à participação comunitária e à análise das áreas observadas.

#### 1.4.2 Objetivos específicos

1. **Delimitar** os trechos e o público da atividade, mediante reconhecimento da área e diálogo com possíveis participantes externos.
2. **Padronizar** os registros de campo, por meio de um protocolo de fotografias, coordenadas, tipos de resíduos e níveis de acúmulo.
3. **Disponibilizar** os recursos do sistema para cadastro, visualização e acompanhamento das ocorrências, mediante implementação e verificação técnica do protótipo.
4. **Registrar** ocorrências reais com os participantes, mediante visitas aos trechos definidos e uso do formulário e do mapa.
5. **Avaliar** a utilização do sistema, por meio da observação de tarefas, análise dos registros e levantamento de dificuldades dos participantes.
6. **Sistematizar** os resultados e as devolutivas, por meio de indicadores, exportações e relatório destinado à comunidade e à instituição.

A implementação técnica já realizada antecedeu a aplicação em campo. A sequência dos objetivos orienta a execução completa da atividade de extensão, incluindo a revisão do protótipo conforme as necessidades identificadas com o público externo.

### 1.5 JUSTIFICATIVA

A organização de informações sobre resíduos em igarapés pode favorecer a identificação de recorrências e o acompanhamento de trechos observados. O sistema reúne localização, fotografia, classificação e histórico em uma mesma ferramenta, oferecendo apoio a atividades educativas e ao planejamento de observações ambientais.

As fontes documentais reunidas na seção 2 contextualizam a relevância territorial da proposta. A demanda específica da comunidade, os parceiros externos e suas contrapartidas ainda precisam ser formalizados na etapa de articulação; não há registro de parceria firmada ou de validação comunitária concluída neste relatório.

## 2 REFERENCIAL TEÓRICO

O objetivo de apoiar o monitoramento colaborativo requer a compreensão do contexto ambiental e da organização de registros georreferenciados. A base documental abaixo reúne fontes jornalísticas e institucionais já presentes no projeto. A revisão de artigos científicos sobre monitoramento participativo, geotecnologias e classificação de resíduos permanece pendente; portanto, esta seção constitui uma fundamentação inicial, a ser aprofundada.

### 2.1 CONTEXTO DOS IGARAPÉS URBANOS DE MANAUS

A cidade de Manaus é cortada por cerca de mil igarapés, organizados em quatro grandes bacias urbanas: Educandos, São Raimundo, Puraquequara e Tarumã-Açu. Do grupo que corta a zona urbana — aproximadamente 150 igarapés — a maioria encontra-se em situação crítica: poluição grave, esgoto sem tratamento e acúmulo de resíduos sólidos, tendo perdido usos históricos como banho, lazer e navegação. O descarte irregular transforma muitos trechos em canais de detritos.

A contaminação é agravada pela falta de saneamento. Estudos apontam que apenas cerca de 22% do esgoto gerado em Manaus é tratado, colocando a capital entre os municípios com piores índices de saneamento entre as cidades mais populosas do país. O esgoto não tratado e o lixo descartado de forma irregular chegam diretamente aos corpos d'água, e pesquisas detectam microplásticos em bacias urbanas importantes, como o Igarapé do Mindu e o Quarenta. Em contraste, o Igarapé Água Branca é considerado um dos últimos trechos urbanos em estado mais preservado.

A poluição também se manifesta em riscos à saúde pública. Em ambientes contaminados, proliferam doenças como diarreia, leptospirose e dengue. A presença de criadouros naturais em balneários e margens de igarapés, por sua vez, eleva o risco de transmissão da malária em áreas vulneráveis: a cidade registrou 4.748 casos entre janeiro e agosto de 2026, com focos de infecção concentrados em localidades próximas a rios, igarapés e áreas de mata.

O quadro se agrava no período de estiagem. Com a descida do nível do Rio Negro, grandes volumes de lixo acumulado nas margens e nos leitos ficam expostos [1], o que motiva frentes de limpeza emergencial e ações de dragagem, como a que retirou cerca de 900 metros cúbicos de lixo e sedimentos no igarapé do Tarumã-Açu. O acúmulo de resíduos compromete ainda a drenagem das águas, elevando o risco de alagamentos durante fortes chuvas.

Como resposta parcial a esse cenário, a prefeitura utiliza tecnologias como as ecobarreiras em pontos específicos, como no Passeio do Mindu, para reter parte dos resíduos sólidos antes que cheguem aos rios principais.

Figura 1 – Registro fotográfico de igarapé urbano de Manaus

![Registro fotográfico de igarapé urbano de Manaus](docs/obsidian/07%20-%20Relatório/igarape1.jpeg)

Fonte: produção própria (acervo do projeto).

### 2.2 RELAÇÃO ENTRE O CONTEXTO AMBIENTAL E AS FUNCIONALIDADES

As informações apresentadas fundamentam diretamente as decisões de escopo e as funcionalidades já implementadas:

- **Registro georreferenciado de ocorrências**: a necessidade de registrar o descarte irregular com tipo de resíduo, nível de acúmulo, data e coordenadas é coerente com o problema descrito. Os tipos adotados (`Plastico`, `Metal`, `Vidro`, `Organico`, `Papel`, `Misto` e `Outro`) abrangem os resíduos citados nas fontes, como garrafas plásticas e embalagens.
- **Pontos monitorados**: o seed do banco apresenta trechos demonstrativos do Mindu, Educandos, Quarenta e Tarumã-Açu, cursos d'água associados às bacias urbanas de Manaus. As coordenadas adicionadas para Quarenta e Tarumã-Açu são referências cartográficas do OpenStreetMap; a localização e os níveis de acúmulo devem ser validados em campo e não constituem classificação ambiental oficial.
- **Níveis de acúmulo e criticidade**: a escala `Baixo`, `Medio` e `Alto` e o filtro de criticidade (nível `Alto`) permitem priorizar os trechos que se tornam canais de detritos ou que acumulam lixo exposto na estiagem, apoiando o direcionamento de ações de limpeza e dragagem.
- **Recorrência e histórico**: o conceito de ponto recorrente (três ou mais ocorrências) e o histórico por ponto respondem à dinâmica real de reincidência do descarte, documentada pela necessidade de operações contínuas da Semulsp e da Seminf.
- **Fotografia e observações**: a documentação visual das ocorrências apoia o registro de resíduos sólidos visíveis e permite acompanhar a evolução de um mesmo trecho ao longo do tempo.
- **Dashboard e exportação**: os indicadores e as exportações em CSV e GeoJSON fornecem subsídios para análises semelhantes às realizadas em pesquisas citadas sobre contaminação e saneamento.

Figura 2 – Registro fotográfico de acúmulo de resíduos em igarapé urbano

![Registro fotográfico de acúmulo de resíduos em igarapé urbano](docs/obsidian/07%20-%20Relatório/igarape2.jpeg)

Fonte: produção própria (acervo do projeto).

### 2.3 IMPLICAÇÕES PARA A PESQUISA DE CAMPO

As fontes também orientam a pesquisa de campo descrita na seção 3: a área inicial de monitoramento deve considerar as bacias mencionadas (Mindu e Educandos) e os riscos à saúde associados, e a coleta deve prever o registro de trechos em período de estiagem, quando o acúmulo fica mais exposto. A comparação de ocorrências antes e depois das operações de limpeza e das ecobarreiras pode ainda fundamentar análises de efetividade no dashboard.

## 3 METODOLOGIA

A atividade articula desenvolvimento incremental de software, levantamento documental e aplicação de campo prevista com a comunidade externa. A etapa técnica encontra-se implementada; a coleta ambiental formal e a avaliação com participantes ainda não foram executadas.

### 3.1 PROCEDIMENTOS E INSTRUMENTOS METODOLÓGICOS

O sistema foi desenvolvido com backend em Python e Flask 3.1, banco de dados SQLite e frontend em HTML, CSS e JavaScript puro, utilizando Leaflet e OpenStreetMap para o mapa e Chart.js para os gráficos. A arquitetura é organizada em camadas — rotas, serviços, repositórios, integrações externas e utilitários — o que favorece a manutenção e a validação independente de cada componente.

A metodologia de desenvolvimento seguiu um plano incremental em etapas, com modelagem do banco, implementação do backend, construção do frontend e do mapa, e posterior evolução em fases de monitoramento, gestão, dados, qualidade e documentação. A verificação das entregas foi realizada por meio de testes automatizados e de registros de evolução documentados no histórico do projeto.

O sistema também integra adaptadores externos auxiliares: hidrografia via Overpass, meteorologia via Open-Meteo, geocodificação reversa via Nominatim e um gateway JSON de sensores com exportação em CSV.

Na etapa de campo, a equipe deverá definir os trechos de atuação em Manaus com os participantes, verificar as condições de acesso e identificar eventuais autorizações necessárias. O protocolo de coleta deverá estabelecer a posição de registro, a data, a fotografia, o tipo de resíduo, o nível de acúmulo e as observações. Os critérios de classificação deverão ser validados antes da coleta controlada.

A questão orientadora da avaliação será: em que medida os participantes conseguem registrar e consultar ocorrências de resíduos com o sistema? Serão observados o preenchimento dos campos, a localização registrada, a qualidade das fotografias e as dificuldades nas tarefas. Os instrumentos previstos são o formulário de ocorrência, o mapa, o histórico por ponto, o dashboard e uma ficha de avaliação de uso a elaborar.

A divulgação e o convite ao público serão organizados após a definição dos parceiros e dos locais. Caso sejam incluídas entrevistas ou coleta de dados de participantes, os procedimentos de consentimento e eventuais exigências institucionais de avaliação ética deverão ser definidos antes dessa coleta.

#### 3.1.1 Público envolvido

A equipe executora é composta pelos quatro integrantes identificados na capa, com orientador ainda a informar. O público externo previsto compreende moradores dos arredores dos trechos selecionados, representantes de grupos ambientais e outros colaboradores locais interessados no monitoramento dos igarapés. Estudantes e pesquisadores também poderão utilizar a ferramenta.

O número estimado de participantes externos, suas instituições representativas e os critérios de participação ainda serão definidos na articulação de campo. Não há quantitativo de beneficiários ou participação externa realizada documentado até o momento.

#### 3.1.2 Plano de trabalho, atividades vinculadas aos objetivos e etapas

O plano abaixo vincula as atividades ao objetivo geral de apoiar o monitoramento colaborativo. A necessidade de autorização para acesso aos locais e execução das atividades deverá ser verificada antes das visitas.

Quadro 1 – Plano de trabalho do projeto de extensão

| Objetivo específico | Atividades vinculadas | Etapa | Situação |
|---|---|---|---|
| 1. Delimitar os trechos e o público | Articular participantes; reconhecer trechos; definir área e verificar autorizações de acesso. | 1 | Pendente |
| 2. Padronizar os registros | Elaborar e validar protocolo de fotografia, localização e classificação; aprofundar a fundamentação científica. | 2 | Pendente |
| 3. Disponibilizar os recursos do sistema | Modelar o banco; implementar backend, mapa, formulários, gestão, indicadores e exportações; verificar segurança e documentar. | 3 | Implementação técnica concluída; adequações de campo previstas |
| 4. Registrar ocorrências reais | Apresentar a ferramenta aos participantes e executar coletas controladas nos trechos definidos. | 4 | Pendente |
| 5. Avaliar a utilização | Observar tarefas, verificar registros e levantar dificuldades e sugestões de uso. | 5 | Pendente |
| 6. Sistematizar os resultados | Analisar indicadores, consolidar exportações, realizar devolutiva e complementar o relatório. | 6 | Relatório em elaboração; análise de campo e devolutiva pendentes |

Fonte: elaborado pelos autores com base no planejamento do projeto.

#### 3.1.3 Cronograma das etapas do projeto

Não foram informadas datas de início e término por etapa. O quadro apresenta a sequência de execução e a situação registrada, sem atribuir meses retrospectivos ou prazos não confirmados. As datas deverão ser preenchidas após definição da agenda com os participantes.

Quadro 2 – Cronograma das etapas do projeto

| Etapa do Quadro 1 | Período de execução | Dependência e situação |
|---|---|---|
| 1 – Delimitação e articulação | A definir | Antes das visitas e da mobilização para coleta |
| 2 – Protocolo e fundamentação | A definir | Após delimitação dos trechos e antes da coleta |
| 3 – Desenvolvimento técnico | Já realizado; datas não informadas | Protótipo disponível; revisão conforme etapas 1 e 2 |
| 4 – Coleta colaborativa | A definir | Após etapas 1 e 2 e apresentação do sistema |
| 5 – Avaliação de uso | A definir | Durante e após a etapa 4 |
| 6 – Sistematização e devolutiva | A definir | Após coleta e avaliação; relatório já iniciado |

Fonte: elaborado pelos autores.

### 3.2 ACOMPANHAMENTO E AVALIAÇÃO

O desenvolvimento é acompanhado por um quadro no Trello, documentação técnica e histórico do projeto. A suíte atual possui 38 testes automatizados para páginas, autenticação, permissões, filtros, exportações, privacidade, segurança, acessibilidade, limpeza, protocolo e migração. Essa verificação técnica deverá ser complementada pela avaliação em campo.

Figura 3 – Quadro de gestão do projeto no Trello

![Quadro de gestão do projeto no Trello](docs/obsidian/07%20-%20Relatório/trello.jpeg)

Fonte: produção própria (acervo do projeto).

A avaliação de campo deverá reunir dados quantitativos, como número de participantes, ocorrências registradas, registros completos e tarefas concluídas, e dados qualitativos, como dificuldades, sugestões e percepção de utilidade. Serão utilizados os registros do sistema e a ficha de avaliação de uso. As metas e os critérios de sucesso serão definidos antes da aplicação, em conjunto com o público envolvido.

A equipe confrontará as atividades realizadas com os objetivos do Quadro 1. A comunidade deverá participar da avaliação e receber uma devolutiva dos registros e das melhorias propostas, em formato acessível a ser combinado com os participantes.

## 4 PROTAGONISMO DA COMUNIDADE EXTERNA

A comunidade externa é o público principal da atividade de extensão prevista. A proposta contempla sua participação na escolha dos trechos, na adequação da linguagem e dos critérios de registro, na coleta de ocorrências e na avaliação do sistema. O conhecimento local poderá orientar a identificação de pontos de descarte recorrente e as condições de acesso aos locais.

Essa participação ainda será articulada. Não se afirma que moradores ou organizações já validaram o protótipo. A equipe deverá registrar as contribuições recebidas, discutir os resultados com os participantes e incorporar as adequações pertinentes, estabelecendo uma relação de troca entre a instituição e a comunidade.

## 5 RELAÇÃO ENSINO, PESQUISA E EXTENSÃO

O ensino está presente na aplicação de conhecimentos de programação, banco de dados, interfaces, geolocalização, testes e documentação. A pesquisa compreende o levantamento de fontes, a definição dos critérios de observação e a análise dos registros. A extensão se concretizará no diálogo e na utilização da ferramenta com a comunidade externa, com devolutiva e revisão a partir das necessidades locais.

Essas dimensões se articulam: as observações dos participantes poderão orientar melhorias técnicas, enquanto a análise dos registros poderá apoiar atividades educativas e novas questões de investigação.

O enquadramento temático proposto é **Biodiversidade**, na linha **Sociobiodiversidade e Meio Ambiente**, conforme as opções do modelo. Esse enquadramento deverá ser validado pela orientação, considerando o curso efetivo da equipe, ainda não informado. Como área de conhecimento, propõe-se Ciência da Computação, com enfoque em desenvolvimento de sistemas de informação aplicados ao monitoramento ambiental; a classificação institucional e a subárea do CNPq permanecem a confirmar.

A proposta se relaciona tematicamente aos ODS 6 (Água potável e saneamento), 11 (Cidades e comunidades sustentáveis) e 12 (Consumo e produção responsáveis), pela organização de informações sobre corpos d'água urbanos e descarte de resíduos. Essa relação expressa a finalidade da proposta; o impacto concreto dependerá da execução e avaliação da atividade.

## 6 RESULTADOS ESPERADOS

O protótipo funcional constitui o resultado técnico já obtido. Os resultados sociais e ambientais esperados dependem da aplicação em campo. Os registros atuais do banco são dados de demonstração e de teste, e não resultados de coleta ambiental formal.

### 6.1 ENTREGAS TÉCNICAS JÁ REALIZADAS

#### 6.1.1 Fundamentos (MVP)

- Definição do escopo: nome do projeto, objetivo geral, objetivos específicos, público-alvo, tipos de resíduos, níveis de acúmulo e dados a serem armazenados.
- Backend Flask com API CRUD de ocorrências e upload de fotografias.
- Banco SQLite com tabelas de usuários, pontos monitorados e ocorrências, incluindo dados seed de teste.
- Frontend com páginas renderizadas via Jinja e integração do mapa Leaflet.
- Registro de ocorrência com geolocalização, seleção manual no mapa ou ponto monitorado.

#### 6.1.2 Monitoramento e mapa

- Página de ponto monitorado com resumo, distribuições, recorrência e histórico.
- Filtros combináveis por tipo, nível, ponto, período e texto.
- Agrupamento de marcadores com MarkerCluster e diferenciação visual por nível de acúmulo.
- Exibição de ocorrências de nível alto (criticidade) e centralização no ponto selecionado.
- Lista recente e exportações sincronizadas com o recorte de filtros do mapa.

#### 6.1.3 Gestão

- Autenticação com login, logout e sessão autenticada.
- Perfis de usuário: `usuario`, `moderador` e `administrador`.
- Status de ocorrência: `Nova`, `Em analise`, `Em atendimento`, `Resolvida` e `Descartada`.
- CRUD de ocorrências e gestão de pontos monitorados conforme permissão.
- Denúncias com protocolo único `IG-AAAA-NNNNNN` e consulta pública de acompanhamento sem identificação do denunciante.
- Avaliação humana da acessibilidade dos trechos, com nível, observações, data e responsável, alterável por moderadores e administradores.
- Histórico próprio de limpezas por ponto, independente do status de ocorrência; a reincidência conta ocorrências posteriores à última operação registrada.

#### 6.1.4 Dados e exportação

- Dashboard com totais gerais, ocorrências nos últimos 7 e 30 dias, pontos ativos e recorrentes.
- Indicadores reais de denúncias pendentes, limpezas registradas, reincidência após a última limpeza e pontos classificados como dificultosos.
- Gráficos por tipo, nível, evolução temporal e ranking de pontos.
- Exportação em CSV e GeoJSON, inclusive com os filtros aplicados.

#### 6.1.5 Qualidade e segurança

- Senhas armazenadas com hash do Werkzeug.
- Cookies `HttpOnly`, `SameSite=Lax` e `Secure` por ambiente.
- Cabeçalhos HTTP de segurança (`X-Content-Type-Options`, `X-Frame-Options` e `Referrer-Policy`).
- Validação de coordenadas, domínios, tamanhos de campos e conteúdo real de imagens com Pillow.
- Limite de 10 MB por requisição.
- Respostas públicas sem `senha_hash` ou `usuario_id`.
- Logs de autenticação e operações sem dados sensíveis.
- Suíte com 38 testes automatizados aprovados, com banco e uploads temporários, incluindo acessibilidade, limpeza, reincidência, protocolo, migração e privacidade.

#### 6.1.6 Interface e documentação

- Identidade visual temática com paleta de floresta, água, argila e areia.
- Layouts responsivos para desktop, tablet e celular.
- Acessibilidade com skip link, foco visível, regiões ARIA e suporte a `prefers-reduced-motion`.
- Documentação técnica navegável no Obsidian e documentos `README`, `ARQUITETURA`, `APRESENTACAO` e `TODO`.

### 6.2 RESULTADOS ACADÊMICOS E SOCIAIS ESPERADOS

Espera-se a constituição de um conjunto inicial de registros reais, com fotografias, localização e histórico dos trechos selecionados, e a identificação de melhorias no sistema a partir de sua utilização pela comunidade. A consulta e a exportação desses registros poderão subsidiar atividades educativas e análises locais sobre o descarte recorrente.

Para os participantes, espera-se ampliar o acesso a informações organizadas sobre os locais observados e a possibilidade de contribuir com o acompanhamento. Para a equipe e o CIESA, espera-se aprofundar a aprendizagem pela aplicação social dos conhecimentos e pela produção de documentação sobre a experiência. A devolutiva deverá favorecer a troca entre academia e sociedade. A redução de resíduos ou a melhoria da qualidade da água não foi medida e não constitui resultado comprovado do protótipo.

## 7 LIMITAÇÕES DA ATIVIDADE DE EXTENSÃO

A pesquisa de campo, a validação dos critérios de classificação e os testes com participantes externos permanecem pendentes. As fotografias incluídas neste documento pertencem ao acervo já disponível; não substituem uma coleta controlada com protocolo, localização e datas documentadas. A revisão científica também precisa ser aprofundada.

A participação depende da articulação com a comunidade, da disponibilidade dos envolvidos e das condições de acesso aos trechos. Conectividade, precisão da localização em dispositivos móveis, qualidade das imagens e diferenças de interpretação dos níveis de acúmulo poderão afetar os registros. Observações limitadas a determinados trechos e períodos não permitem generalização para todos os igarapés de Manaus. Fotografias de resíduos visíveis não comprovam contaminação microbiológica ou por microplásticos.

Como limitações técnicas, destacam-se o uso de SQLite e armazenamento local de imagens para cenários de alta concorrência; a ausência de migrações versionadas, recuperação de senha e proteção CSRF dedicada; e a possibilidade de um usuário autenticado atualizar ocorrências que não criou. O acompanhamento por protocolo não autentica o cidadão e, por isso, as respostas não incluem dados pessoais. A classificação de acessibilidade é humana, ainda sem protocolo de avaliação de campo; as operações e quantidades de limpeza são registros inseridos por operadores, não comprovação independente. A implantação em produção ainda não foi realizada. O encerramento do projeto depende da coleta, avaliação, aprofundamento científico e complementação do relatório.

## 8 RECURSOS

Os recursos humanos compreendem os quatro integrantes da equipe e a orientação acadêmica a definir. A participação de colaboradores externos será acordada durante a articulação comunitária. Não foram informadas bolsas, remuneração específica, financiamento ou contrapartidas de parceiros.

Os recursos materiais previstos incluem computadores, dispositivos com câmera e localização, acesso à internet e infraestrutura para execução do sistema. Sua disponibilidade para a etapa de campo deverá ser confirmada. O software utiliza Python/Flask, SQLite, HTML, CSS, JavaScript e as bibliotecas descritas na metodologia.

Quadro 3 – Recursos humanos, materiais e financeiros

| Categoria | Recurso ou despesa | Quantidade | Fonte ou disponibilidade | Destinação | Valor estimado |
|---|---|---|---|---|---|
| Humano | Integrantes da equipe | 4 | Equipe identificada na capa | Desenvolvimento, campo, avaliação e relatório | Remuneração específica não informada |
| Humano | Orientação acadêmica | A definir | CIESA; responsável a informar | Orientação e acompanhamento | Não informado |
| Humano | Participantes externos | A definir | Articulação comunitária pendente | Definição dos trechos, registros e avaliação | Não informado |
| Material | Computadores | A confirmar | Disponibilidade para a equipe a confirmar | Desenvolvimento, análise e documentação | A levantar |
| Material | Dispositivos com câmera e localização | A confirmar | Disponibilidade para campo a confirmar | Fotografias e registros georreferenciados | A levantar |
| Serviço | Internet e eventual hospedagem | A dimensionar | Fonte de custeio a definir | Acesso, envio de imagens e disponibilização | A levantar |
| Logística | Deslocamentos e materiais de campo | A dimensionar | Fonte de custeio a definir | Visitas aos trechos selecionados | A levantar |

Fonte: elaborado pelos autores.

Não há orçamento financeiro consolidado. Quantidades, custos unitários, total e fontes de custeio deverão ser definidos após a escolha dos trechos e do número de participantes. Valores não informados não representam custo zero.

## REFERÊNCIAS

1. ALMEIDA FILHO, Paulo. **Os igarapés que cortam Manaus**. Manaus: Associação Comercial do Amazonas, 18 abr. 2023. Disponível em: https://aca.org.br/os-igarapes-que-cortam-manaus/. Acesso em: 22 set. 2026.

2. SOUZA, Almir. **Os igarapés esquecidos de Manaus**. Manaus: Olhar do Norte Brasil, 20 mar. 2026. Disponível em: https://www.olhardonortebrasil.com.br/os-igarapes-esquecidos-de-manaus/. Acesso em: 22 set. 2026.

3. MOTA E SILVA, Tiago da. **Dos igarapés aos manguezais, microplásticos contaminam a Amazônia**. Mongabay Brasil, 26 jun. 2026. Disponível em: https://brasil.mongabay.com/2026/06/dos-igarapes-aos-manguezais-microplasticos-contaminam-a-amazonia/. Acesso em: 22 set. 2026.

4. MANAUS. Prefeitura Municipal. Secretaria Municipal de Saúde. **Prefeitura de Manaus reforça alerta sobre risco de transmissão de malária em balneários e locais favoráveis aos criadouros naturais do mosquito Anopheles**. Manaus, 14 set. 2026. Disponível em: https://www.manaus.am.gov.br/semsa/alerta-risco-transmissao-malaria/. Acesso em: 22 set. 2026.

5. VLAXIO, Elanny. **As ecobarreiras podem salvar os igarapés de Manaus?** Amazônia Latitude, 19 jun. 2024. Disponível em: https://www.amazonialatitude.com/2024/06/19/ecobarreiras-podem-salvar-igarapes-manaus/. Acesso em: 22 set. 2026.

6. MANAUS REFORÇA orientações da Semsa sobre prevenção da malária em balneários e comunidades. **Portal Informe Manaus**, Manaus, 14 set. 2026. Disponível em: https://informemanaus.com.br/manaus-reforca-orientacoes-da-semsa-sobre-prevencao-da-malaria-em-balnearios-e-comunidades/09/. Acesso em: 22 set. 2026.

7. MANAUS. Prefeitura Municipal. Secretaria Municipal de Infraestrutura. **Prefeitura de Manaus retira 900 metros cúbicos de lixo de igarapé durante obra de dragagem e recupera fluxo das águas no Tarumã-Açu**. Manaus, 7 ago. 2026. Disponível em: https://www.manaus.am.gov.br/noticia/servicos/retira-lixo-igarape/. Acesso em: 22 set. 2026.
