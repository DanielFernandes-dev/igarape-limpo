# Arquitetura do Igarapé Vivo

## 1. Estado do documento

| Campo | Valor |
|---|---|
| Versão | 3.0 |
| Estado | Fases 1 a 6 concluídas |
| Próxima fase | Pesquisa e teste de campo |
| Stack | Flask, SQLite, JavaScript, Leaflet e Chart.js |

Este documento descreve o sistema implementado. Itens explicitamente marcados como futuros não fazem parte da versão atual.

## 2. Visão geral

O Igarapé Vivo transforma observações ambientais em ocorrências georreferenciadas. Uma ocorrência pode ser associada a um ponto monitorado, formando um histórico que alimenta mapa, dashboard e exportações.

```text
Navegador
   │
   ├── páginas Jinja + CSS + JavaScript
   ├── Leaflet / MarkerCluster
   └── Chart.js
   │
   ▼
Flask
   ├── pages Blueprint
   ├── API Blueprint
   ├── serviços de domínio
   ├── repositórios SQLite
   ├── integrações externas
   └── utilitários HTTP/exportação
   │
   ├──────────────┐
   ▼              ▼
SQLite       static/uploads
```

Fluxo funcional:

> autenticar → registrar → validar → localizar → visualizar → analisar → acompanhar → exportar

## 3. Organização em camadas

### Apresentação

- Templates em `templates/`.
- Estilos base em `static/css/style.css`.
- Reformulação visual em `static/css/ui.css`.
- JavaScript específico por página em `static/js/`.

### Rotas

- `app/routes/pages.py`: renderização das páginas.
- `app/routes/api.py`: API JSON, multipart, CSV e integrações.

### Serviços

- `auth_service.py`: autenticação, senha e usuários.
- `ocorrencia_service.py`: validação, upload, CRUD, serialização e exportação.
- `ponto_service.py`: regras de pontos, histórico e recorrência.
- `estatistica_service.py`: indicadores, séries e ranking.
- `integracao_service.py`: status das integrações.

### Repositórios

- `usuario_repository.py`.
- `ocorrencia_repository.py`.
- `ponto_repository.py`.

Os repositórios usam consultas parametrizadas por meio de `database.py`.

### Infraestrutura e integrações

- `database.py`: conexão por contexto Flask, inicialização e migrações idempotentes.
- `app/integrations/`: Overpass, Open-Meteo, Nominatim e sensores.
- `app/utils/http.py`: cliente HTTP do backend.
- `app/utils/export.py`: CSV e GeoJSON.

## 4. Estrutura atual

```text
igarape-limpo/
├── app.py                         # entry point
├── config.py                      # configuração e domínios
├── database.py                    # SQLite e evolução de schema
├── schema.sql                     # instalação inicial e seed
├── app/
│   ├── __init__.py                # create_app, sessão, headers e erros
│   ├── routes/
│   │   ├── pages.py
│   │   └── api.py
│   ├── services/
│   │   ├── auth_service.py
│   │   ├── ocorrencia_service.py
│   │   ├── ponto_service.py
│   │   ├── estatistica_service.py
│   │   └── integracao_service.py
│   ├── repositories/
│   │   ├── usuario_repository.py
│   │   ├── ocorrencia_repository.py
│   │   └── ponto_repository.py
│   ├── integrations/
│   │   ├── overpass.py
│   │   ├── openmeteo.py
│   │   ├── nominatim.py
│   │   └── sensor_gateway.py
│   └── utils/
│       ├── export.py
│       └── http.py
├── templates/                     # oito páginas Jinja
├── static/
│   ├── css/style.css
│   ├── css/ui.css
│   ├── js/
│   └── uploads/
└── tests/
    ├── conftest.py
    └── test_quality.py
```

## 5. Modelo de dados

### Usuário

Armazena nome, e-mail único, hash de senha, perfil, estado ativo e data de criação.

Perfis:

- `usuario`: registra e consulta.
- `moderador`: também gerencia pontos e exclui ocorrências.
- `administrador`: também cria usuários.

### Ponto monitorado

Representa uma referência geográfica estável, com nome, coordenadas, descrição e estado. Seu histórico é composto pelas ocorrências com o mesmo `ponto_id`.

### Ocorrência

Contém localização, data, fotografia opcional, tipo, nível, status, observações e referências opcionais a ponto e usuário.

```text
USUARIO 1 ─────── N OCORRENCIA N ─────── 1 PONTO_MONITORADO
```

O `usuario_id` é persistido para contexto interno e removido das respostas públicas.

## 6. Fluxos implementados

### Registro de ocorrência

1. Usuário autenticado abre `/nova`.
2. Define coordenadas por geolocalização, mapa ou ponto monitorado.
3. Classifica tipo e nível.
4. Opcionalmente seleciona fotografia e visualiza preview local.
5. O frontend bloqueia o botão enquanto envia `multipart/form-data`.
6. O backend valida coordenadas, domínios, tamanhos e ponto associado.
7. Pillow verifica formato e integridade básica da imagem.
8. O arquivo recebe nome UUID e é salvo em `static/uploads`.
9. A ocorrência é associada ao usuário da sessão e persistida.
10. A operação é registrada em log e o navegador abre o detalhe.

### Consulta no mapa

1. O frontend combina filtros e chama `GET /api/ocorrencias`.
2. O backend valida parâmetros e consulta o repositório.
3. O mapa, cards, contagem, lista e URLs de exportação são atualizados sem recarregar a página.
4. Marcadores próximos são clusterizados.

### Histórico e análise

1. O ponto agrega ocorrências por `ponto_id`.
2. O serviço calcula totais e distribuições.
3. Um ponto é recorrente a partir de três ocorrências no histórico total.
4. O dashboard calcula indicadores no backend e os apresenta com Chart.js.

## 7. Interface e experiência

A reformulação UX/UI usa uma camada complementar em `static/css/ui.css` e preserva os contratos DOM consumidos pelos scripts.

### Identidade

- Verde floresta, azul de água, argila e areia.
- Lora para títulos e Manrope para interface.
- Marca com folha e curso d'água.
- Cabeçalho sticky, navegação ativa e identificação da conta.

### Componentes

- Cabeçalhos editoriais por página.
- Cards de indicadores com notas contextuais.
- Painéis para mapa, gráficos, listas e formulários.
- Formulário dividido em localização, classificação e evidência.
- Estados vazios e mensagens de rede.
- Preview de fotografia e loading em ações assíncronas.

### Responsividade e acessibilidade

- Breakpoints em 980, 700 e 420 px.
- Navegação horizontal adaptável e grids reduzidos em telas menores.
- Mapas com alturas adequadas por viewport.
- Skip link, foco visível e `aria-current`.
- Labels associados, `role="status"` e regiões nomeadas.
- Canvas com descrição acessível.
- Suporte a `prefers-reduced-motion`.

Os testes automatizados validam renderização e contratos de backend; validação em dispositivos e tecnologias assistivas reais pertence à Fase 7.

## 8. API e acesso

### Público

- Consulta de ocorrências e pontos.
- Histórico, dashboard e exportações.
- Adaptadores de integração conforme endpoint.

### Autenticado

- Criação e atualização de ocorrência.

### Moderador ou administrador

- Criação e atualização de pontos.
- Exclusão de ocorrência.
- Listagem de usuários.

### Administrador

- Criação de usuário.

Limitação atual: o formulário de status é exibido apenas para moderador/admin, mas o endpoint genérico de atualização aceita status de qualquer usuário autenticado. A autorização de campo deve ser reforçada antes de produção.

## 9. Segurança

Implementado:

- hash de senha do Werkzeug;
- sessão em cookie `HttpOnly` e `SameSite=Lax`;
- `Secure` por `IGARAPE_HTTPS=1`;
- segredo configurável por `IGARAPE_SECRET_KEY`;
- headers contra MIME sniffing e framing;
- validação de entradas e consultas parametrizadas;
- limite de 10 MB;
- inspeção de imagens por extensão e Pillow;
- nomes UUID;
- respostas sem hashes e identificadores internos desnecessários;
- logs sem senha ou token;
- erro 500 genérico na API.

Pendente para produção:

- CSRF dedicado;
- política de credenciais e recuperação de senha;
- auditoria persistente de alterações;
- propriedade de ocorrência;
- remoção de metadados e otimização de imagem;
- allowlist para destinos do gateway de sensores.

## 10. Integrações externas

Adaptadores e endpoints implementados:

- Overpass para hidrografia;
- Open-Meteo para meteorologia;
- Nominatim para geocodificação reversa;
- gateway JSON de sensores;
- exportação de sensores em CSV;
- endpoint de status das integrações.

O backend executa as chamadas, evitando CORS no navegador. Porém, o gateway ainda recebe URL e token do cliente. O painel visual de integrações e a configuração exclusivamente no servidor permanecem futuros.

Falhas externas retornam `502` e não impedem acesso ao banco, páginas e mapa base.

## 11. Exportação e interoperabilidade

CSV contém dados tabulares de ocorrências. GeoJSON representa cada ocorrência como `Feature` com geometria `Point` em ordem longitude/latitude.

Ambos aceitam os filtros da listagem. O frontend atualiza automaticamente os links de exportação conforme o recorte do mapa.

## 12. Testes

A suíte atual possui 20 testes e usa banco e uploads temporários.

Cobertura existente:

- páginas principais;
- autenticação válida e inválida;
- proteção de criação;
- filtros;
- dashboard;
- CSV e GeoJSON;
- privacidade de respostas;
- ocorrência sem fotografia;
- PNG válido e arquivo falso;
- limite `413`;
- headers de segurança.

Ainda são desejáveis testes de autorização por campo, integrações externas simuladas, JavaScript em navegador, acessibilidade automatizada e dispositivos reais.

## 13. Decisões e trade-offs

- SQLite reduz complexidade, mas limita concorrência.
- Imagens locais facilitam a demonstração, mas não escalam horizontalmente.
- JavaScript puro evita um framework adicional, mas exige disciplina nos contratos DOM.
- CDNs simplificam Leaflet, Chart.js e fontes, mas introduzem dependência de rede.
- Migrações idempotentes simples atendem o protótipo, mas não substituem ferramenta versionada.
- Recorrência por limiar é compreensível, mas ainda não possui validação ambiental.

## 14. Implantação

O comando atual inicia o servidor de desenvolvimento Flask. Antes de produção:

1. usar servidor WSGI;
2. definir `IGARAPE_SECRET_KEY` persistente;
3. servir somente por HTTPS e ativar `IGARAPE_HTTPS=1`;
4. trocar a credencial seed;
5. restringir integrações externas;
6. usar banco e armazenamento apropriados;
7. implementar backups, observabilidade e migrações versionadas.

## 15. Roadmap atual

### Fase 7 — próxima

- definir área inicial e fontes;
- validar metodologia e classificação;
- realizar coleta controlada;
- testar localização, fotografia, conexão e dispositivos;
- avaliar usabilidade e registrar correções;
- diferenciar resultados técnicos de resultados ambientais.

### Produção

- autorização rigorosa, CSRF e recuperação de acesso;
- PostgreSQL/PostGIS e armazenamento de objetos;
- imagens otimizadas e sem metadados;
- integrações configuradas no servidor;
- auditoria persistente.

### Futuro

- índice de criticidade calibrado;
- visão computacional após formação de conjunto de dados;
- alertas após validação de tendências históricas.

## 16. Critérios atendidos

O protótipo já permite registrar, associar, filtrar, visualizar, acompanhar, analisar e exportar ocorrências com arquitetura em camadas, autenticação e validações.

O sucesso ambiental e metodológico ainda não pode ser avaliado: depende da Fase 7 e de dados reais coletados sob protocolo validado.
