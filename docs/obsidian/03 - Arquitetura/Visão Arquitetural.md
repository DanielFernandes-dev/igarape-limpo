---
tags:
  - arquitetura
  - visão-geral
tipo: técnico
status: atual
---

# Visão Arquitetural

## Estilo

O Igarapé Limpo é uma aplicação web monolítica Flask, renderizada no servidor e complementada por JavaScript sem framework no navegador.

```mermaid
flowchart TB
    subgraph Browser[Navegador]
        J[Jinja / HTML]
        C[CSS]
        JS[JavaScript por página]
        L[Leaflet / MarkerCluster]
        CH[Chart.js]
    end

    subgraph Flask[Aplicação Flask]
        P[Rotas de páginas]
        A[Rotas da API]
        S[Serviços]
        R[Repositórios]
        I[Integrações]
        U[Utilitários]
    end

    DB[(SQLite)]
    UP[(static/uploads)]
    EXT[Serviços externos]

    Browser --> P
    Browser --> A
    P --> S
    A --> S
    S --> R
    S --> I
    S --> U
    R --> DB
    S --> UP
    I --> EXT
```

## Componentes

| Camada | Responsabilidade | Local |
|---|---|---|
| Inicialização | Factory, sessão, headers e erros | `app/__init__.py` |
| Páginas | Renderização Jinja | `app/routes/pages.py` |
| API | HTTP, JSON, multipart e exportações | `app/routes/api.py` |
| Serviços | Validação e regras de negócio | `app/services/` |
| Repositórios | Consultas SQL parametrizadas | `app/repositories/` |
| Integrações | Adaptação de serviços externos | `app/integrations/` |
| Persistência | Conexão, schema e evolução | `database.py`, `schema.sql` |
| Interface | Templates e assets | `templates/`, `static/` |

## Estrutura principal

```text
igarape-limpo/
├── app.py
├── config.py
├── database.py
├── schema.sql
├── app/
│   ├── __init__.py
│   ├── routes/
│   ├── services/
│   ├── repositories/
│   ├── integrations/
│   └── utils/
├── templates/
├── static/
│   ├── css/
│   ├── js/
│   └── uploads/
└── tests/
```

## Fluxo de uma requisição

```mermaid
sequenceDiagram
    participant N as Navegador
    participant R as Rota Flask
    participant S as Serviço
    participant P as Repositório
    participant D as SQLite
    N->>R: Requisição HTTP
    R->>S: Dados normalizados
    S->>S: Validação e regras
    S->>P: Operação de persistência
    P->>D: SQL parametrizado
    D-->>P: Resultado
    P-->>S: Registro
    S-->>R: Objeto serializável
    R-->>N: JSON, HTML ou arquivo
```

## Decisões e trade-offs

- Flask e JavaScript puro reduzem a complexidade inicial.
- SQLite facilita demonstração local, mas limita concorrência e escala.
- Upload local é simples, mas impede escalabilidade horizontal direta.
- Separar rotas, serviços e repositórios mantém regras fora do transporte HTTP.
- Leaflet e OpenStreetMap evitam chave comercial.
- CDNs simplificam os assets, mas tornam parte da interface dependente de rede.
- Evoluções idempotentes em `database.py` atendem o protótipo, mas não substituem migrações versionadas.

## Notas relacionadas

- [[Backend]]
- [[Frontend]]
- [[Modelo de Dados]]
- [[Implantação]]
