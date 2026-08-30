---
tags:
  - arquitetura
  - frontend
  - interface
tipo: técnico
status: atual
---

# Frontend

## Composição

A interface é renderizada com Jinja e usa JavaScript específico por página. Não há SPA, bundler, TypeScript ou framework frontend.

`templates/base.html` concentra:

- metadados;
- dependências por CDN;
- navegação e identidade da conta;
- logout;
- skip link e rodapé;
- blocos Jinja de conteúdo, estilos e scripts.

## Páginas

| Rota | Template | Finalidade |
|---|---|---|
| `/` | `index.html` | Mapa, filtros e lista |
| `/nova` | `nova_ocorrencia.html` | Cadastro de ocorrência |
| `/ocorrencia/<id>` | `ocorrencia.html` | Detalhe e status |
| `/ponto/<id>` | `ponto.html` | Histórico do ponto |
| `/dashboard` | `dashboard.html` | Indicadores e gráficos |
| `/login` | `login.html` | Autenticação |
| ocorrência/ponto ausente | `nao_encontrado.html` | Resposta 404 específica |

O template de não encontrado não é um handler global para qualquer URL inválida.

## JavaScript

| Arquivo | Responsabilidade |
|---|---|
| `static/js/map.js` | Mapa principal, filtros, clusters, lista e exportação |
| `static/js/main.js` | Formulário, mapa de seleção, geolocalização e preview |
| `static/js/dashboard.js` | Consultas e gráficos Chart.js |
| `static/js/detalhe.js` | Mapa de uma ocorrência |
| `static/js/ponto.js` | Mapa de um ponto |

Os scripts dependem de IDs, classes e atributos específicos dos templates. Alterações no HTML devem preservar esses contratos ou atualizar o JavaScript correspondente.

## Estilos

- `static/css/style.css`: estilos base históricos;
- `static/css/ui.css`: identidade visual e reformulação responsiva.

A interface usa Lora para títulos e Manrope para controles e leitura, com fallbacks locais.

## Dependências externas

- Leaflet 1.9.4 via unpkg;
- Leaflet.markercluster 1.5.3 via unpkg;
- Chart.js 4.4.1 via jsDelivr;
- tiles do OpenStreetMap;
- Google Fonts.

Sem acesso à internet, as páginas locais podem abrir, mas mapas, fontes e gráficos não funcionam integralmente.

## Responsividade

Os principais breakpoints estão em 980, 700 e 420 px. Grids, navegação, formulários e altura dos mapas se ajustam para tablet e celular.

## Acessibilidade implementada

- skip link;
- foco visível;
- `aria-current` na navegação;
- labels associados aos controles;
- regiões `aria-live` e status;
- nomes acessíveis para mapas e gráficos;
- suporte a `prefers-reduced-motion`.

> [!note] Cobertura
> A estrutura possui recursos de acessibilidade, mas ainda precisa de avaliação com tecnologias assistivas e dispositivos reais.

## Segurança no navegador

O conteúdo dinâmico de popups e listas passa por sanitização no frontend. Isso complementa, mas não substitui, validação e escape no servidor.

## Lacunas funcionais

Não há telas completas para:

- criar ou editar pontos;
- listar ou criar usuários;
- excluir ocorrências;
- configurar e visualizar integrações externas.

Essas operações existem total ou parcialmente na [[API HTTP]].
