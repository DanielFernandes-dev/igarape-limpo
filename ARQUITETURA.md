# Relatório de Arquitetura — Igarapé Vivo

## 1. Identificação do documento

| Campo | Valor |
|-------|-------|
| **Projeto** | Igarapé Vivo |
| **Documento** | Relatório de Arquitetura do Protótipo — Evolução consolidada (MVP + V2) |
| **Versão** | 2.0 |
| **Status** | Em desenvolvimento |
| **Objetivo** | Descrever a arquitetura do protótipo evoluído, consolidando o MVP existente (implementado) e as novas funcionalidades de monitoramento, análise, acompanhamento e gestão das ocorrências. |

> **Nota de consolidação:** este documento substitui a versão 1.0 do relatório e reúne em um único arquivo o conteúdo do MVP implementado e a proposta de evolução V2. As seções marcadas com **(implementado)** descrevem o que já existe em execução; as demais descrevem a evolução planejada.

---

## 2. Visão geral

O **Igarapé Vivo** é um sistema de monitoramento colaborativo de resíduos sólidos em corpos d'água urbanos. O protótipo permite o registro, o georreferenciamento e a visualização de ocorrências de resíduos, transformando observações ambientais dispersas em dados organizados.

A proposta central do projeto, conforme descrita no README, é:

> *"Transformar observações sobre resíduos em dados georreferenciados que possam ser visualizados, comparados e acompanhados ao longo do tempo."*

A evolução mantém o fluxo central do MVP:

> **registrar → armazenar → localizar → visualizar**

E amplia esse fluxo para:

> **registrar → validar → localizar → visualizar → analisar → acompanhar → comparar → exportar**

A nova arquitetura passa a considerar, além da ocorrência individual, o conceito de **ponto monitorado**, permitindo acompanhar recorrência, histórico e situação de cada local ao longo do tempo.

O sistema continua destinado a estudantes, pesquisadores, projetos de extensão, grupos ambientais e comunidades próximas a igarapés.

---

## 3. Objetivos da arquitetura

A arquitetura foi ampliada para preservar a simplicidade do MVP e preparar o sistema para crescimento funcional.

### 3.1. Objetivos funcionais

1. Permitir o cadastro de ocorrências de resíduos;
2. Armazenar a localização geográfica de cada ocorrência;
3. Permitir o envio e a visualização de fotografias;
4. Classificar o tipo de resíduo e o nível de acúmulo;
5. Apresentar as ocorrências em mapa interativo;
6. Permitir consulta detalhada de cada ocorrência;
7. Permitir filtros e pesquisa no mapa;
8. Agrupar ocorrências visualmente quando houver muitos marcadores;
9. Criar e acompanhar pontos monitorados;
10. Manter histórico de ocorrências por ponto;
11. Identificar pontos com ocorrências recorrentes;
12. Acompanhar o status de uma ocorrência;
13. Apresentar indicadores e gráficos analíticos;
14. Permitir exportação dos dados para análise externa;
15. Preparar a arquitetura para autenticação e controle de acesso;
16. Servir de base para visão computacional, alertas e integrações futuras.

### 3.2. Objetivos não funcionais

- Manter baixa complexidade no núcleo do sistema;
- Separar apresentação, regras de negócio, persistência e serviços;
- Validar dados de entrada no backend;
- Melhorar a segurança de arquivos enviados;
- Preparar a aplicação para evolução do banco de dados;
- Facilitar manutenção, testes e futuras integrações.

---

## 4. Funcionalidades

### 4.1. Funcionalidades existentes do MVP **(implementado)**

- Cadastro de ocorrência;
- Seleção de localização no mapa;
- Uso da Geolocation API;
- Classificação do resíduo;
- Classificação do nível de acúmulo;
- Upload de fotografia;
- Persistência em SQLite;
- Visualização em mapa Leaflet;
- Popup resumido;
- Página de detalhe;
- Cards básicos de resumo;
- Lista de ocorrências recentes.

### 4.2. Funcionalidades adicionadas na evolução

- Filtros por tipo de resíduo;
- Filtros por nível de acúmulo;
- Filtros por período;
- Pesquisa por local;
- Visualização de pontos críticos;
- Agrupamento de marcadores no mapa;
- Dashboard analítico;
- Gráficos temporais e por categoria;
- Ponto monitorado;
- Histórico por ponto;
- Detecção de recorrência;
- Status da ocorrência;
- Fluxo de acompanhamento;
- Exportação CSV;
- Preparação para GeoJSON;
- Autenticação e perfis de usuário;
- Controle de edição e exclusão;
- Validação reforçada de imagens;
- Estrutura preparada para serviços de análise futura.

---

## 5. Stack tecnológica

A stack existente é mantida como base do protótipo, com possibilidade de substituição gradual de componentes quando a escala exigir.

| Camada | Tecnologia / proposta | Justificativa | Status |
|--------|-----------------------|---------------|--------|
| **Frontend** | HTML, CSS e JavaScript puro | Simplicidade e compatibilidade com o MVP | Implementado |
| **Backend** | Python + Flask | Leve e adequado ao protótipo | Implementado |
| **API** | HTTP + JSON / multipart | Integração frontend-backend | Implementado |
| **Banco atual** | SQLite | Simples para desenvolvimento e validação | Implementado |
| **Banco futuro** | PostgreSQL + extensão espacial, se necessário | Maior concorrência e consultas geográficas em escala | Planejado |
| **Mapa** | Leaflet + OpenStreetMap | Código aberto e adequado à visualização geográfica | Implementado |
| **Clusterização** | Plugin de agrupamento do Leaflet | Reduz sobreposição de marcadores | Planejado |
| **Imagens** | Armazenamento local (`static/uploads`) | Simples no ambiente do protótipo | Implementado |
| **Imagens futuro** | Armazenamento de objetos / serviço externo | Escalabilidade e maior disponibilidade | Planejado |
| **Exportação** | CSV inicialmente; GeoJSON posteriormente | Interoperabilidade com ferramentas de análise | Planejado |

A visão computacional, os alertas automáticos e o monitoramento por câmeras continuam fora do escopo imediato desta versão.

---

## 6. Integrações com serviços externos (referência AcquaVig)

Esta seção documenta as integrações com serviços externos previstas para o Igarapé Vivo, tendo como referência o painel **AcquaVig** (monitoramento ambiental e hidrológico). Elas estão em **proposta de evolução** — nenhuma foi implementada nesta fase.

### 6.1. Visão geral

O objetivo é enriquecer o monitoramento com dados contextuais (cartografia, hidrografia, meteorologia e sensores), mantendo o princípio de simplicidade e tratando as chamadas externas de forma segura.

> **Regra transversal:** todas as chamadas a serviços externos devem ser feitas **pelo backend Flask**, evitando problemas de CORS e, principalmente, a exposição de credenciais no navegador (o painel AcquaVig usa `localStorage`, o que não é recomendado para produção).

### 6.2. Integrações propostas

| # | Integração | Serviço | Uso no Igarapé Vivo | Status |
|---|-----------|---------|----------------------|--------|
| 1 | **Cartografia base** | OpenStreetMap via Leaflet | Exibição do mapa, marcadores e popups | **Já em uso (MVP)** |
| 2 | **Hidrografia** | Overpass API (dados OSM) | Carregar igarapés/rios/canais do OpenStreetMap e relacionar as ocorrências aos cursos d'água (`waterway` = river/stream/canal) | Planejado |
| 3 | **Meteorologia** | Open-Meteo | Temperatura, umidade, chuva, vento e previsão de precipitação (próximas horas) para o contexto de Manaus, permitindo correlação com ocorrências | Planejado |
| 4 | **Geocodificação reversa** | Nominatim | Converter as coordenadas de uma ocorrência em nome de local (bairro/subdistrito) no registro | Planejado |
| 5 | **Telemetria de qualidade da água** | Gateway de sensores (endpoint JSON configurável) | pH, turbidez, temperatura da água, oxigênio dissolvido e condutividade, com marcadores, tabela e exportação | Planejado |
| 6 | **Geolocalização do usuário** | Geolocation API | Obter a localização atual no registro da ocorrência | **Já em uso (MVP)** |
| 7 | **Dados hidrológicos oficiais** | ANA HidroWebService (referência futura) | Dados hidrológicos de fontes oficiais — integrar sempre pelo backend, sem credenciais no frontend | Futuro |

### 6.3. Detalhamento das integrações

#### 6.3.1. Hidrografia (Overpass API)

Consulta os cursos d'água do OpenStreetMap dentro de uma área delimitada e os desenha como linhas no mapa, diferenciando-os das ocorrências.

- Fonte: `Overpass API` (com fallback entre endpoints);
- Consulta: `way["waterway"~"river|stream|canal"]["name"]` dentro do bounding box da área monitorada;
- Uso: destacar os igarapés e permitir identificar quais ocorrências estão em sua proximidade;
- Paginação/limite: limitar o número de trechos e nomes únicos para manter a consulta leve.

#### 6.3.2. Meteorologia (Open-Meteo)

Fornece condições atuais e previsão horária de precipitação para a região (Manaus).

- Parâmetros: temperatura, umidade relativa, precipitação, chuva, velocidade do vento, código meteorológico e probabilidade de precipitação;
- Uso: adicionar contexto pluviométrico ao painel e possível correlação com o surgimento/deslocamento de resíduos;
- Visualização: gráfico de barras com a precipitação das próximas horas, como no AcquaVig;
- Fuso: `America/Manaus`.

#### 6.3.3. Geocodificação reversa (Nominatim)

Converte latitude/longitude em uma descrição de local legível.

- Parâmetros: `format=jsonv2`, `lat`, `lon`, `zoom`, `accept-language=pt-BR`;
- Uso: preencher automaticamente o campo `local_nome` (ou um bairro) ao registrar uma ocorrência, reduzindo digitação manual;
- Limite de uso: respeitar a política de uso do Nominatim (1 requisição/segundo, com identificação).

#### 6.3.4. Telemetria de sensores (gateway configurável)

Permite conectar um endpoint JSON real com estações de qualidade da água, exibindo somente dados que existam de fato.

- Estrutura esperada: lista/objeto `stations` com `id`, `name`, `lat`, `lon`, `ph`, `turbidity_ntu`, `water_temperature_c`, `dissolved_oxygen_mg_l`, `conductivity_us_cm`, `updated_at`;
- Autenticação: suporte a token do tipo `Bearer`;
- **Segurança:** a configuração (URL + token) deve ficar no **backend**, e não no `localStorage` como no painel de referência;
- Uso: visualizar estações e seus parâmetros no mapa e em tabela, com exportação;
- Estado vazio: quando nenhum endpoint for configurado, exibir aviso de que não há telemetria.

#### 6.3.5. Exportação CSV

Exportar as ocorrências (e posteriormente a telemetria) em CSV, compatível com ferramentas de análise.

- Colunas sugeridas das ocorrências: `id`, `data_hora`, `latitude`, `longitude`, `tipo_residuo`, `nivel_acumulo`, `status`, `local_nome`, `ponto_id`, `observacoes`;
- Implementação: via endpoint da API ou geração no cliente;
- Essa integração reforça a exportação já prevista na evolução (seção de Exportação e interoperabilidade).

### 6.4. Painel de status das integrações

A interface deve apresentar um painel de status das fontes externas, semelhante ao "Integrações" do AcquaVig, com estados:

- **ativo** — serviço respondendo normalmente;
- **consultando** — chamada em andamento;
- **sob demanda** — acionado apenas quando necessário;
- **erro/indisponível** — falha na consulta (mantendo o mapa base e as ocorrências em funcionamento).

### 6.5. Decisões de arquitetura

- Chamadas externas realizadas **pelo backend** (Flask), com tratamento de erros e mensagens amigáveis ao usuário;
- Configurações sensíveis (ex.: token do gateway) armazenadas no **servidor**, nunca em código público ou no armazenamento do navegador;
- **Gradualidade:** cada integração independente — se um serviço falhar, os demais (e o MVP) continuam operando;
- A integração com a **ANA** e a **visão computacional** permanecem em repouso para fases posteriores, conforme o roadmap.

---

## 7. Visão arquitetural

```text
Usuário
   │
   ▼
Navegador (Frontend HTML/CSS/JS)
   │
   ├── Formulário de ocorrência
   ├── Mapa interativo
   ├── Filtros e pesquisa
   ├── Dashboard
   └── Detalhes / histórico
   │
   ▼
Servidor Flask
   │
   ├── Rotas de páginas
   ├── API REST/JSON
   ├── Autenticação e autorização
   ├── Validação de dados
   ├── Serviço de ocorrências
   ├── Serviço de pontos monitorados
   ├── Serviço de estatísticas
   ├── Serviço de exportação
   └── Serviço de upload
   │
   ├──────────────────────┐
   ▼                      ▼
Banco de dados         Armazenamento
SQLite inicialmente    de imagens
   │
   └──────────────┬───────────────┐
                  ▼               ▼
             Dashboard         Exportações
                  │
                  ▼
            Análises futuras
```

---

## 8. Organização em camadas

A arquitetura evoluída separa as responsabilidades para evitar que as regras de negócio se concentrem em `app.py`.

| Camada | Responsabilidade |
|--------|------------------|
| **Apresentação** | Interface, formulários, mapa, filtros e dashboard |
| **Rotas** | Receber requisições HTTP e devolver páginas/JSON |
| **Serviços** | Regras de negócio e casos de uso |
| **Repositórios** | Acesso ao banco de dados |
| **Domínio / modelos** | Entidades e estruturas de dados |
| **Infraestrutura** | Banco, arquivos, autenticação e configurações |

### 7.1. Estrutura atual **(implementado)**

```text
igarape-limpo/
│
├── app.py                     # Aplicação Flask (rotas, API e upload)
├── config.py                  # Configurações (banco, uploads, constantes)
├── database.py                # Conexão e helpers de acesso ao SQLite
├── schema.sql                 # Criação de tabela e dados de exemplo (seed)
├── requirements.txt           # Dependências Python
├── README.md                  # Documentação geral do projeto
├── TODO.MD                    # Lista de etapas de desenvolvimento
├── ARQUITETURA.md             # Este relatório
│
├── /static
│   ├── /css/style.css         # Estilos do aplicativo
│   ├── /js/map.js             # Mapa da página inicial
│   ├── /js/main.js            # Formulário de registro
│   ├── /js/detalhe.js         # Mini-mapa de detalhe
│   └── /uploads/              # Fotografias enviadas (ignoradas no Git)
│
└── /templates
    ├── base.html              # Layout base
    ├── index.html             # Página inicial: mapa + resumo + lista
    ├── nova_ocorrencia.html   # Formulário de registro
    ├── ocorrencia.html        # Detalhe de uma ocorrência
    └── nao_encontrado.html    # Página 404
```

### 7.2. Estrutura sugerida para a evolução

```text
igarape-limpo/
│
├── app.py
├── config.py
├── requirements.txt
├── README.md
├── TODO.md
├── schema.sql
│
├── app/
│   ├── routes/
│   │   ├── pages.py
│   │   └── api.py
│   │
│   ├── services/
│   │   ├── ocorrencia_service.py
│   │   ├── ponto_service.py
│   │   ├── estatistica_service.py
│   │   ├── exportacao_service.py
│   │   ├── upload_service.py
│   │   └── auth_service.py
│   │
│   ├── repositories/
│   │   ├── ocorrencia_repository.py
│   │   ├── ponto_repository.py
│   │   └── usuario_repository.py
│   │
│   ├── models/
│   │   ├── ocorrencia.py
│   │   ├── ponto_monitorado.py
│   │   └── usuario.py
│   │
│   └── utils/
│       ├── validators.py
│       └── pagination.py
│
├── database.py
│
├── static/
│   ├── css/
│   ├── js/
│   │   ├── map.js
│   │   ├── main.js
│   │   ├── detalhe.js
│   │   ├── dashboard.js
│   │   └── filtros.js
│   └── uploads/
│
└── templates/
    ├── base.html
    ├── index.html
    ├── nova_ocorrencia.html
    ├── ocorrencia.html
    ├── ponto.html
    ├── dashboard.html
    ├── login.html
    └── nao_encontrado.html
```

---

## 9. Modelo de dados

O modelo atual possui uma única tabela de ocorrências. Para a nova fase, são introduzidas entidades auxiliares (`usuarios` e `pontos_monitorados`).

### 8.1. Entidade `usuarios`

| Campo | Tipo | Descrição |
|------|------|-----------|
| `id` | INTEGER | Identificador |
| `nome` | TEXT | Nome do usuário |
| `email` | TEXT | Identificador de acesso |
| `senha_hash` | TEXT | Senha armazenada de forma segura |
| `perfil` | TEXT | Papel do usuário |
| `ativo` | INTEGER | Indica se o usuário está ativo |
| `data_criacao` | TEXT | Data de criação |

Perfis previstos:

- `usuario` — registra ocorrências e consulta dados;
- `moderador` — revisa e atualiza ocorrências;
- `administrador` — gerencia usuários e configurações.

### 8.2. Entidade `pontos_monitorados`

| Campo | Tipo | Descrição |
|------|------|-----------|
| `id` | INTEGER | Identificador |
| `nome` | TEXT | Nome do ponto |
| `latitude` | REAL | Latitude |
| `longitude` | REAL | Longitude |
| `descricao` | TEXT | Características do local |
| `status` | TEXT | Situação do ponto |
| `data_criacao` | TEXT | Data de cadastro |

### 8.3. Entidade `ocorrencias` **(implementada, sem `ponto_id`/`usuario_id`/`status`/`data_atualizacao`)**

| Campo | Tipo | Descrição |
|------|------|-----------|
| `id` | INTEGER | Identificador único |
| `ponto_id` | INTEGER | Ponto monitorado relacionado |
| `usuario_id` | INTEGER | Usuário responsável pelo registro |
| `latitude` | REAL | Latitude da ocorrência |
| `longitude` | REAL | Longitude da ocorrência |
| `data_hora` | TEXT | Data e hora do registro |
| `fotografia` | TEXT | Caminho/nome da imagem |
| `tipo_residuo` | TEXT | Tipo de resíduo |
| `nivel_acumulo` | TEXT | Nível de acúmulo |
| `status` | TEXT | Estado do acompanhamento |
| `observacoes` | TEXT | Informações adicionais |
| `local_nome` | TEXT | Nome de referência do local |
| `data_atualizacao` | TEXT | Última atualização |

> A tabela `ocorrencias` **implementada** contém atualmente: `id`, `latitude`, `longitude`, `data_hora`, `fotografia`, `tipo_residuo`, `nivel_acumulo`, `observacoes` e `local_nome`. Os campos `ponto_id`, `usuario_id`, `status` e `data_atualizacao` serão acrescentados na evolução, junto com o índice espacial já existente.

### 8.4. Domínios controlados

**Tipos de resíduo:**

`Plastico`, `Metal`, `Vidro`, `Organico`, `Papel`, `Misto`, `Outro`

**Níveis de acúmulo:**

`Baixo`, `Medio`, `Alto`

**Status de ocorrência:**

`Nova`, `Em analise`, `Em atendimento`, `Resolvida`, `Descartada`

**Status do ponto monitorado:**

`Ativo`, `Inativo`

---

## 10. Relacionamentos

```text
USUARIO
   │
   └──────────< OCORRENCIA >────────── PONTO_MONITORADO
                     │
                     └──── fotografia / histórico
```

Relacionamentos principais:

- Um usuário pode registrar várias ocorrências;
- Um ponto monitorado pode possuir várias ocorrências;
- Uma ocorrência pode estar associada a um ponto monitorado;
- O histórico de um ponto é composto pelas ocorrências relacionadas a ele.

---

## 11. Fluxo de registro

### 10.1. Fluxo implementado no MVP **(implementado)**

1. O usuário acessa `/nova` e preenche o formulário;
2. A localização é obtida pela **Geolocation API** (botão) ou por **clique no mapa**;
3. O resíduo é classificado (tipo e nível de acúmulo) e, opcionalmente, anexa-se uma fotografia;
4. O formulário envia os dados como `multipart/form-data` (via `fetch` + `FormData`) para `POST /api/ocorrencias`;
5. O backend **valida** coordenadas, tipo, nível e extensão da imagem;
6. A foto (se houver) é salva em `static/uploads/` com nome único (`ocorr_<uuid>.<ext>`);
7. Os dados são inseridos no banco SQLite;
8. O usuário é redirecionado para a página de detalhe da nova ocorrência.

### 10.2. Fluxo de registro aprimorado (evolução)

```text
1. Localização
      ↓
2. Classificação do resíduo
      ↓
3. Nível de acúmulo
      ↓
4. Fotografia
      ↓
5. Observações
      ↓
6. Revisão dos dados
      ↓
7. Envio
      ↓
8. Validação no backend
      ↓
9. Persistência
      ↓
10. Página da ocorrência
```

#### 10.2.1. Melhorias de UX

- Preview da fotografia antes do envio;
- Mensagem de localização obtida;
- Validação imediata de campos;
- Mensagens de erro contextuais;
- Indicador de progresso;
- Estado de carregamento durante o upload;
- Confirmação após o cadastro;
- Possibilidade de revisar os dados antes de enviar.

---

## 12. Mapa interativo

### 11.1. Implementado no MVP **(implementado)**

O mapa utiliza **Leaflet** com o provedor de tiles **OpenStreetMap**.

- Página inicial (`index.html` + `map.js`): circula o mapa na área de monitoramento, carrega as ocorrências via `GET /api/ocorrencias`, renderiza cada uma como um **círculo colorido** conforme o nível de acúmulo, exibe popup resumido, cards de resumo e lista de recentes;
- Página de registro (`nova_ocorrencia.html` + `main.js`): mapa seletor — clicar marca o ponto, e o botão "Usar minha localização" aciona a Geolocation API;
- Página de detalhe (`ocorrencia.html` + `detalhe.js`): mini-mapa centralizado na ocorrência com círculo colorido.

### 11.2. Mapa evoluído (planejado)

O mapa passa a ser o principal ambiente de exploração dos dados, com:

- Marcadores por ocorrência;
- Cor por nível de acúmulo;
- Popup com resumo;
- Filtro por tipo de resíduo;
- Filtro por nível;
- Filtro por período;
- Pesquisa por local;
- Exibição apenas de pontos críticos;
- Centralização no ponto selecionado;
- Agrupamento (clusterização) de marcadores;
- Acesso ao detalhe;
- Acesso ao histórico do ponto.

### 11.3. Legenda

| Nível | Cor |
|-------|-----|
| Baixo | `#22c55e` |
| Médio | `#eab308` |
| Alto | `#ef4444` |

### 11.4. Exibição de pontos críticos

O usuário poderá ativar um filtro que mostre somente ocorrências classificadas com nível `Alto`.

Futuramente, o conceito de ponto crítico poderá considerar uma combinação de:

- quantidade de ocorrências;
- recorrência;
- nível de acúmulo;
- período recente.

---

## 13. Pesquisa e filtros

Os filtros devem ser combináveis.

Exemplo:

```text
Tipo: Plástico
Nível: Alto
Período: Últimos 30 dias
Local: Igarapé do Mindu
```

O resultado deve atualizar:

- mapa;
- contagem de resultados;
- lista de ocorrências;
- indicadores do dashboard.

A aplicação deve evitar recarregamentos completos de página quando a alteração puder ser feita via API.

---

## 14. Dashboard analítico

O dashboard amplia o resumo atual para uma camada de análise.

### 13.1. Indicadores

- Total de ocorrências;
- Ocorrências nos últimos 7 dias;
- Ocorrências nos últimos 30 dias;
- Pontos monitorados ativos;
- Pontos críticos;
- Resíduo mais frequente;
- Local com maior número de ocorrências;
- Ocorrências recorrentes.

> No MVP **(implementado)**, o resumo é calculado no lado do cliente (cards: ocorrências registradas, pontos monitorados, maior ocorrência e pontos críticos), sem persistência de histórico.

### 13.2. Gráficos

- Ocorrências por tipo de resíduo;
- Ocorrências por nível de acúmulo;
- Evolução de ocorrências ao longo do tempo;
- Ranking dos pontos mais críticos;
- Distribuição por local;
- Comparação entre períodos.

### 13.3. Regra de consistência

Os indicadores devem ser calculados preferencialmente no backend quando a quantidade de dados crescer, evitando transferência desnecessária de todos os registros para o navegador.

---

## 15. Histórico por ponto monitorado

Cada ponto monitorado possuirá uma página dedicada contendo:

- nome do ponto;
- localização no mapa;
- quantidade de ocorrências;
- última ocorrência;
- distribuição por tipo de resíduo;
- distribuição por nível;
- histórico temporal;
- status atual;
- fotografias recentes;
- indicação de recorrência.

Exemplo de interpretação:

> "Este ponto apresentou 12 ocorrências nos últimos 3 meses e registrou nível alto de acúmulo em 4 ocasiões."

O objetivo é permitir comparação do estado ambiental do mesmo local ao longo do tempo.

---

## 16. Recorrência e pontos críticos

A versão evoluída deve identificar locais com repetição de ocorrências.

Uma regra inicial simples pode considerar:

```text
Ponto recorrente = ponto com quantidade de ocorrências acima de um limite
                   em uma determinada janela de tempo.
```

A regra poderá evoluir posteriormente para um índice de criticidade.

Exemplo conceitual:

```text
criticidade = frequência + intensidade + recência
```

A fórmula definitiva deve ser validada com dados reais antes de ser adotada como métrica oficial.

---

## 17. Status e acompanhamento das ocorrências

Cada ocorrência pode seguir um ciclo de vida:

```text
Nova
  ↓
Em análise
  ↓
Em atendimento
  ↓
Resolvida
```

Fluxos alternativos:

```text
Nova → Descartada
Em análise → Descartada
```

### 16.1. Permissões sugeridas

| Ação | Usuário | Moderador | Administrador |
|------|---------|-----------|---------------|
| Criar ocorrência | Sim | Sim | Sim |
| Consultar | Sim | Sim | Sim |
| Editar própria ocorrência | Conforme regra | Sim | Sim |
| Alterar status | Não | Sim | Sim |
| Excluir | Não | Conforme regra | Sim |
| Gerenciar usuários | Não | Não | Sim |

---

## 18. API evoluída

### 17.1. Ocorrências

| Método | Rota | Descrição | Status |
|--------|------|-----------|--------|
| GET | `/api/ocorrencias` | Lista ocorrências com filtros | Implementado (sem filtros) |
| GET | `/api/ocorrencias/<id>` | Consulta ocorrência | Implementado |
| POST | `/api/ocorrencias` | Cria ocorrência | Implementado |
| PATCH | `/api/ocorrencias/<id>` | Atualiza ocorrência | Planejado |
| DELETE | `/api/ocorrencias/<id>` | Remove ocorrência conforme permissão | Planejado |

### 17.2. Pontos monitorados

| Método | Rota | Descrição |
|--------|------|-----------|
| GET | `/api/pontos` | Lista pontos |
| GET | `/api/pontos/<id>` | Consulta ponto |
| POST | `/api/pontos` | Cria ponto |
| PATCH | `/api/pontos/<id>` | Atualiza ponto |
| GET | `/api/pontos/<id>/historico` | Histórico do ponto |

### 17.3. Dashboard

| Método | Rota | Descrição |
|--------|------|-----------|
| GET | `/api/dashboard/resumo` | Indicadores gerais |
| GET | `/api/dashboard/series` | Séries temporais |
| GET | `/api/dashboard/ranking` | Ranking de pontos |

### 17.4. Exportação

| Método | Rota | Descrição |
|--------|------|-----------|
| GET | `/api/export/ocorrencias.csv` | Exporta ocorrências em CSV |
| GET | `/api/export/ocorrencias.geojson` | Exporta ocorrências em GeoJSON |

### 17.5. Páginas

| Método | Rota | Descrição | Status |
|--------|------|-----------|--------|
| GET | `/` | Página inicial (mapa + resumo) | Implementado |
| GET | `/nova` | Formulário de registro | Implementado |
| GET | `/ocorrencia/<id>` | Detalhe de uma ocorrência | Implementado |
| GET | `/ponto/<id>` | Página do ponto monitorado | Planejado |
| GET | `/dashboard` | Dashboard analítico | Planejado |
| GET | `/login` | Acesso de usuário | Planejado |

---

## 19. Filtros da API

Exemplo:

```text
GET /api/ocorrencias?
    tipo_residuo=Plastico&
    nivel_acumulo=Alto&
    data_inicio=2026-01-01&
    data_fim=2026-01-31&
    ponto_id=3
```

O backend deve validar todos os parâmetros antes de executar consultas.

---

## 20. Upload e segurança das imagens

O protótipo atual valida extensão e tamanho. A evolução deve adicionar validação do conteúdo real do arquivo.

### 19.1. Implementado **(implementado)**

- Limite de tamanho configurável (10 MB);
- Extensões permitidas (png, jpg, jpeg, gif, webp);
- Geração de nome único (`ocorr_<uuid>.<ext>`);
- Não utilização do nome enviado pelo usuário como caminho final.

### 19.2. Regras planejadas

- Validação MIME/content type;
- Armazenamento fora da área de execução quando possível;
- Restrição de tipos de arquivo executáveis;
- Possibilidade de redimensionamento/compressão;
- Registro de falhas no upload.

### 19.3. Estrutura de armazenamento proposta

```text
static/uploads/
├── 2026/
│   ├── 08/
│   └── 09/
```

A estrutura por data pode facilitar organização e manutenção quando o volume crescer.

---

## 21. Autenticação e autorização

A autenticação passa a ser uma funcionalidade da evolução do sistema.

### 20.1. Autenticação

- Login por e-mail e senha;
- Senhas armazenadas com hash seguro;
- Sessão autenticada;
- Logout;
- Recuperação de acesso em fase posterior.

### 20.2. Autorização

As operações devem verificar o perfil antes de permitir alterações sensíveis.

Exemplo:

```text
POST /api/ocorrencias
        ↓
usuário autenticado?
        ↓
      sim
        ↓
validar payload
        ↓
criar ocorrência
```

---

## 22. Validação e tratamento de erros

| Situação | Comportamento | Status |
|----------|----------------|--------|
| Coordenadas inválidas | HTTP 400 | Implementado |
| Tipo de resíduo inválido | HTTP 400 | Implementado |
| Nível de acúmulo inválido | HTTP 400 | Implementado |
| Status inválido | HTTP 400 | Planejado |
| Arquivo não permitido | HTTP 400 | Implementado |
| Arquivo muito grande | HTTP 413 | Implementado |
| Não autenticado | HTTP 401 | Planejado |
| Sem permissão | HTTP 403 | Planejado |
| Recurso inexistente (detalhe/API) | HTTP 404 | Implementado |
| Erro interno | HTTP 500 | Planejado |
| Dados duplicados | HTTP 409 quando aplicável | Planejado |

As mensagens para o usuário devem ser amigáveis, enquanto detalhes técnicos devem permanecer nos logs do servidor.

> No MVP **(implementado)**, a injeção SQL é mitigada pelo uso de parâmetros vinculados nas consultas do `database.py`.

---

## 23. Prevenção de duplicidade

O sistema deve reduzir o registro repetido da mesma ocorrência.

Uma primeira estratégia pode verificar:

- proximidade geográfica;
- intervalo de tempo;
- tipo de resíduo;
- nível de acúmulo.

Exemplo conceitual:

```text
Nova ocorrência
      ↓
Buscar ocorrências próximas e recentes
      ↓
Existe possível duplicata?
   ↙             ↘
 sim             não
  ↓               ↓
Avisar usuário   Criar
```

Essa regra deve ser implementada de forma orientativa inicialmente, evitando bloquear registros válidos.

---

## 24. Índices e desempenho

Índices atuais e previstos:

```sql
CREATE INDEX idx_ocorrencias_coord
ON ocorrencias (latitude, longitude);   -- implementado

CREATE INDEX idx_ocorrencias_data
ON ocorrencias (data_hora);

CREATE INDEX idx_ocorrencias_tipo
ON ocorrencias (tipo_residuo);

CREATE INDEX idx_ocorrencias_nivel
ON ocorrencias (nivel_acumulo);

CREATE INDEX idx_ocorrencias_ponto
ON ocorrencias (ponto_id);

CREATE INDEX idx_ocorrencias_status
ON ocorrencias (status);
```

Quando houver necessidade de consultas espaciais mais avançadas ou alta concorrência, poderá ser avaliada migração para PostgreSQL com suporte espacial.

---

## 25. Exportação e interoperabilidade

### 24.1. CSV

Campos sugeridos:

```text
id,
data_hora,
latitude,
longitude,
tipo_residuo,
nivel_acumulo,
status,
local_nome,
ponto_id,
observacoes
```

### 24.2. GeoJSON

O GeoJSON deve representar cada ocorrência como uma `Feature` com geometria `Point`.

Exemplo conceitual:

```json
{
  "type": "Feature",
  "geometry": {
    "type": "Point",
    "coordinates": [-60.040980, -3.059860]
  },
  "properties": {
    "tipo_residuo": "Plastico",
    "nivel_acumulo": "Alto",
    "status": "Nova"
  }
}
```

---

## 26. Frontend

### 25.1. `index.html`

Página principal com:

- mapa;
- filtros;
- indicadores;
- lista de ocorrências;
- acesso aos pontos monitorados.

### 25.2. `nova_ocorrencia.html`

Formulário orientado em etapas, mapa seletor e preview da fotografia.

### 25.3. `ocorrencia.html`

Detalhe da ocorrência, fotografia, localização, status e informações do registro.

### 25.4. `ponto.html`

Resumo, mapa, histórico, estatísticas e ocorrências relacionadas ao ponto.

### 25.5. `dashboard.html`

Indicadores, gráficos, filtros e rankings.

### 25.6. `login.html`

Acesso de usuários autenticados.

---

## 27. Usabilidade e acessibilidade

A interface deve evoluir para:

- boa leitura em dispositivos móveis;
- botões com área de toque adequada;
- contraste suficiente;
- labels associados aos campos;
- mensagens de erro próximas ao campo correspondente;
- navegação possível por teclado;
- estados visuais de carregamento;
- não depender exclusivamente de cor para indicar criticidade.

A legenda do mapa deve continuar apresentando texto além das cores.

---

## 28. Observabilidade e logs

A aplicação deve registrar eventos importantes, como:

- criação de ocorrência;
- atualização de status;
- falha de upload;
- tentativa de acesso não autorizado;
- erros de banco;
- erros inesperados da API.

Não devem ser registrados em log:

- senhas;
- tokens sensíveis;
- informações pessoais desnecessárias.

---

## 29. Testes

### 28.1. Testes de backend

- Validação de coordenadas;
- Validação de domínios;
- Criação de ocorrência;
- Atualização de status;
- Consulta por filtros;
- Histórico por ponto;
- Exportação;
- Permissões.

### 28.2. Testes de frontend

- Seleção de localização;
- Geolocation API;
- Preview de imagem;
- Filtros;
- Atualização do mapa;
- Exibição de erros;
- Responsividade.

### 28.3. Testes de integração

- Cadastro completo de ocorrência;
- Upload + persistência;
- Ocorrência associada a ponto;
- Atualização de status;
- Dashboard com dados persistidos.

---

## 30. Dados de exemplo

O `schema.sql` deve continuar oferecendo dados de teste para o ambiente de desenvolvimento.

> **Seed atual (implementado):** o `schema.sql` pré-popula 5 ocorrências no Igarapé do Mindu com diferentes tipos de resíduo e níveis de acúmulo, permitindo validar imediatamente a diferenciação visual dos marcadores no mapa. O banco (`igarape_vivo.db`) e a pasta de uploads são criados automaticamente na primeira execução.

A seed evoluída deve contemplar:

- diferentes tipos de resíduo;
- diferentes níveis;
- diferentes datas;
- diferentes pontos monitorados;
- ocorrências recorrentes;
- diferentes status;
- usuários fictícios para validação da autenticação.

---

## 31. Instalação e execução

```bash
# 1. Criar ambiente virtual
python3 -m venv .venv

# 2. Instalar dependências
.venv/bin/pip install -r requirements.txt

# 3. Iniciar o servidor
.venv/bin/python app.py
```

Acesse `http://127.0.0.1:5000`.

---

## 32. Evolução planejada

| Versão | Foco |
|--------|------|
| **V1 — MVP** | Registro, localização, fotografia, classificação, armazenamento, mapa e consulta (implementado) |
| **V2 — Monitoramento** | Filtros, dashboard, pontos monitorados, histórico e recorrência |
| **V2.1 — Gestão** | Status, autenticação, permissões e melhoria de segurança |
| **V2.2 — Dados** | Exportação CSV/GeoJSON e melhorias analíticas |
| **V2.3 — Integrações externas** | Hidrografia (Overpass), meteorologia (Open-Meteo), geocodificação (Nominatim) e telemetria de sensores — referência AcquaVig |
| **V3 — Inteligência** | Classificação automática de resíduos por visão computacional |
| **V4 — Monitoramento automático** | Alertas, câmeras e sensores |

---

## 33. Roadmap recomendado

### Fase 1 — Consolidar a experiência

- Reformular formulário;
- Adicionar preview de foto;
- Adicionar filtros;
- Melhorar mapa;
- Adicionar agrupamento de marcadores.

### Fase 2 — Transformar ocorrências em monitoramento

- Criar ponto monitorado;
- Associar ocorrências aos pontos;
- Implementar histórico;
- Criar recorrência;
- Criar pontos críticos.

### Fase 3 — Transformar dados em análise

- Dashboard;
- Gráficos;
- Ranking;
- Comparação temporal;
- Exportação CSV/GeoJSON.

### Fase 3.5 — Integrações externas (referência AcquaVig)

- Integrar hidrografia via Overpass (cursos d'água do OSM) e relacionar com ocorrências;
- Integrar meteorologia via Open-Meteo (temperatura, umidade, chuva e previsão de precipitação);
- Integrar geocodificação reversa via Nominatim no registro de ocorrência;
- Conectar gateway de sensores de qualidade da água (endpoint JSON, via backend);
- Criar painel de status das integrações;
- Finalizar a exportação de ocorrências/telemetria em CSV;
- Avaliar integração com a ANA HidroWebService pelo backend.

### Fase 4 — Gestão e segurança

- Autenticação;
- Perfis;
- Permissões;
- Validação avançada de imagens;
- Logs;
- Testes automatizados.

### Fase 5 — Inteligência

- Classificação automática por imagem;
- Alertas;
- Integração com dispositivos;
- Câmeras e sensores.

---

## 34. Limitações conhecidas

Mesmo com a evolução proposta, continuam existindo limitações que deverão ser monitoradas:

- SQLite pode limitar concorrência em cenários maiores;
- armazenamento local de imagens não é ideal para produção em escala;
- regras de recorrência precisam de validação com dados reais;
- criticidade ainda é um conceito que deverá ser calibrado;
- exportação GeoJSON exige cuidados de consistência geográfica;
- autenticação e autorização ainda representam uma etapa adicional de implementação;
- visão computacional e monitoramento automático permanecem fora do escopo atual.

**Limitações específicas do MVP já implementado:**

- Sem autenticação/controle de usuários;
- Armazenamento local de imagens e banco;
- Sem validação de conteúdo das imagens (apenas extensão e tamanho);
- Cards de resumo calculados no cliente, sem histórico;
- Sem migrações versionadas de banco;
- Modelo de dados simplificado (sem usuários/pontos/status).

---

## 35. Critérios de sucesso da V2

A versão evoluída será considerada funcional quando permitir:

1. Registrar uma ocorrência com localização, classificação e fotografia;
2. Associar a ocorrência a um ponto monitorado;
3. Consultar ocorrências usando filtros combinados;
4. Visualizar pontos e ocorrências no mapa;
5. Consultar o histórico de um ponto;
6. Identificar pontos recorrentes;
7. Alterar e acompanhar o status das ocorrências conforme a permissão;
8. Visualizar indicadores e gráficos no dashboard;
9. Exportar dados estruturados;
10. Restringir operações sensíveis por autenticação e autorização;
11. Validar uploads de forma mais segura;
12. Manter a arquitetura organizada em camadas.

---

## 36. Conclusão

A arquitetura evoluída mantém a simplicidade do protótipo original, mas amplia seu papel de um sistema de registro para uma plataforma de **monitoramento, análise e acompanhamento de resíduos em corpos d'água urbanos**.

A principal evolução estrutural é a introdução do conceito de **ponto monitorado** e de um histórico associado às ocorrências. Com isso, o sistema passa a permitir não apenas visualizar onde existe um problema, mas também observar sua frequência, recorrência, evolução temporal e situação de acompanhamento.

A arquitetura proposta prepara o projeto para crescer de forma incremental, preservando o MVP enquanto cria uma base para dashboard analítico, gestão de ocorrências, autenticação, exportação de dados e, posteriormente, inteligência computacional e monitoramento automático.
