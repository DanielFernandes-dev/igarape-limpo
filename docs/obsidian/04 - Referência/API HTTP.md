---
tags:
  - api
  - referência
  - http
tipo: referência
status: atual
---

# API HTTP

## Convenções

- Prefixo: `/api`.
- Sucesso: JSON, exceto exportações.
- Erro esperado: `{"erro": "mensagem"}`.
- Autenticação: cookie de sessão Flask.
- Não há JWT nem API key para a API interna.

## Autenticação e usuários

| Método | Endpoint | Acesso | Entrada |
|---|---|---|---|
| `POST` | `/api/auth/login` | Público | JSON com `email` e `senha` |
| `POST` | `/api/auth/logout` | Público | Sem corpo obrigatório |
| `GET` | `/api/auth/me` | Autenticado | - |
| `GET` | `/api/auth/usuarios` | Moderador/Admin | - |
| `POST` | `/api/auth/usuarios` | Admin | JSON de usuário |

### Login

```http
POST /api/auth/login
Content-Type: application/json

{"email":"admin@igarape.local","senha":"admin123"}
```

### Criar usuário

```json
{
  "nome": "Nome da pessoa",
  "email": "pessoa@example.org",
  "senha": "senha-inicial",
  "perfil": "usuario"
}
```

Perfis permitidos: `usuario`, `moderador` e `administrador`.

## Ocorrências

| Método | Endpoint | Acesso | Formato |
|---|---|---|---|
| `GET` | `/api/ocorrencias` | Público | Query string |
| `GET` | `/api/ocorrencias/<id>` | Público | - |
| `POST` | `/api/ocorrencias` | Autenticado | `multipart/form-data` |
| `PUT` | `/api/ocorrencias/<id>` | Autenticado | Formulário/multipart |
| `PATCH` | `/api/ocorrencias/<id>` | Autenticado | JSON parcial ou formulário |
| `DELETE` | `/api/ocorrencias/<id>` | Moderador/Admin | - |

### Filtros de listagem

| Parâmetro | Descrição |
|---|---|
| `tipo_residuo` | Categoria exata |
| `nivel_acumulo` | `Baixo`, `Medio` ou `Alto` |
| `ponto_id` | Identificador numérico do ponto |
| `data_inicio` | Data no formato `AAAA-MM-DD` |
| `data_fim` | Data no formato `AAAA-MM-DD` |
| `busca` | Texto em local e observações |

Exemplo:

```http
GET /api/ocorrencias?nivel_acumulo=Alto&data_inicio=2026-08-01
```

### Criar ocorrência

Campos de formulário:

- `latitude` e `longitude` obrigatórios;
- `tipo_residuo` e `nivel_acumulo` obrigatórios;
- `ponto_id`, `local_nome` e `observacoes` opcionais;
- `fotografia` opcional.

O backend valida extensão e conteúdo real da fotografia. O limite considera a requisição inteira.

### Atualização parcial

```http
PATCH /api/ocorrencias/1
Content-Type: application/json

{"status":"Em analise"}
```

> [!warning] Campos vazios
> Na atualização parcial, valores vazios podem ser removidos durante a mesclagem e preservar o valor existente. A API não oferece um contrato confiável para limpar todos os campos opcionais.

> [!warning] Permissão de status
> O endpoint exige somente autenticação para atualizar. A restrição de status a moderadores e administradores existe na interface, mas não é garantida pelo endpoint genérico.

## Pontos monitorados

| Método | Endpoint | Acesso | Formato |
|---|---|---|---|
| `GET` | `/api/pontos` | Público | - |
| `GET` | `/api/pontos/<id>` | Público | - |
| `POST` | `/api/pontos` | Moderador/Admin | Dados de formulário |
| `PUT`/`PATCH` | `/api/pontos/<id>` | Moderador/Admin | Dados de formulário |
| `GET` | `/api/pontos/<id>/historico` | Público | - |

> [!important] Formato
> A criação e a atualização de pontos leem `request.form`; não envie esses dados como JSON.

Campos: `nome`, `latitude`, `longitude`, `descricao` e `status`.

## Dashboard

| Método | Endpoint | Descrição |
|---|---|---|
| `GET` | `/api/dashboard/resumo` | Totais e distribuições |
| `GET` | `/api/dashboard/series?dias=30` | Série entre 1 e 365 dias |
| `GET` | `/api/dashboard/ranking?limite=10` | Ranking limitado a no máximo 50 itens |

O campo JSON `pontos_criticos` representa pontos recorrentes segundo a regra atual. Veja [[Glossário]].

## Exportações

| Método | Endpoint | Resposta |
|---|---|---|
| `GET` | `/api/export/ocorrencias.csv` | CSV separado por `;` |
| `GET` | `/api/export/ocorrencias.geojson` | GeoJSON `FeatureCollection` |
| `POST` | `/api/export/sensores.csv` | CSV gerado de gateway externo |

As exportações de ocorrências aceitam os mesmos filtros da listagem.

## Integrações

| Método | Endpoint | Entrada |
|---|---|---|
| `GET` | `/api/integracao/hidrografia` | Sem parâmetros obrigatórios |
| `GET` | `/api/integracao/meteo?lat=&lon=` | Latitude e longitude |
| `GET` | `/api/integracao/geocode?lat=&lon=` | Latitude e longitude |
| `POST` | `/api/integracao/sensores` | JSON com `url` e `token` opcional |
| `GET` | `/api/integracao/status` | Sem parâmetros |

`/api/integracao/status` executa chamadas reais aos serviços; não é apenas uma leitura de configuração.

Veja [[Integrações Externas]].

## Privacidade das respostas

As representações públicas removem `senha_hash` e `usuario_id`. O nome interno da fotografia pode aparecer para permitir a URL do arquivo estático.

## Implementação

- Rotas: `app/routes/api.py`.
- Regras: `app/services/`.
- Persistência: `app/repositories/`.
- Exportação: `app/utils/export.py`.
