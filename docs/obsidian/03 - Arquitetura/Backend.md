---
tags:
  - arquitetura
  - backend
  - flask
tipo: técnico
status: atual
---

# Backend

## Inicialização

`app.py` cria a aplicação e inicia o servidor de desenvolvimento com debug habilitado. `app/__init__.py` contém a factory `create_app()` e configura:

- banco e schema;
- blueprints de páginas e API;
- carregamento do usuário da sessão;
- constantes para templates;
- headers de segurança;
- respostas de erro.

## Rotas

### Páginas

`app/routes/pages.py` renderiza as páginas Jinja e busca dados necessários para detalhes de ocorrência e ponto.

### API

`app/routes/api.py` concentra os contratos HTTP:

- autenticação e usuários;
- ocorrências;
- pontos monitorados;
- dashboard;
- exportações;
- integrações externas.

Consulte [[API HTTP]] para métodos e formatos.

## Serviços

| Serviço | Responsabilidade |
|---|---|
| `auth_service.py` | Login, hashing, validação e usuários |
| `ocorrencia_service.py` | CRUD, domínios, upload, serialização e exportação |
| `ponto_service.py` | Pontos, histórico, distribuições e recorrência |
| `estatistica_service.py` | Resumo, séries e ranking |
| `integracao_service.py` | Verificação ativa das integrações |

Os serviços levantam erros de validação e mantêm regras de domínio fora das rotas.

## Repositórios

Os repositórios em `app/repositories/` executam SQL parametrizado:

- `usuario_repository.py`;
- `ocorrencia_repository.py`;
- `ponto_repository.py`.

A conexão é obtida por `database.get_db()` e associada ao contexto da requisição Flask.

## Upload de imagens

1. O serviço valida a extensão.
2. Pillow abre e verifica o conteúdo real.
3. O arquivo recebe um nome UUID.
4. O conteúdo é salvo em `static/uploads`.
5. O banco armazena somente o nome interno.

O limite total por requisição é 10 MiB. Não há redimensionamento nem remoção de metadados.

## Exportações

`app/utils/export.py` transforma ocorrências em:

- CSV separado por `;`;
- GeoJSON `FeatureCollection`.

No GeoJSON, a ordem das coordenadas segue o padrão `[longitude, latitude]`.

## Cliente HTTP

`app/utils/http.py` usa `urllib` da biblioteca padrão para chamadas externas. As integrações convertem falhas conhecidas em erros de gateway, normalmente apresentados como HTTP 502.

## Persistência e inicialização

`database.py`:

- abre a conexão SQLite;
- inicializa o schema;
- aplica evoluções idempotentes simples;
- insere o administrador de desenvolvimento quando necessário.

> [!warning] Chaves estrangeiras
> `schema.sql` executa `PRAGMA foreign_keys = ON`, mas `get_db()` não o habilita explicitamente para cada conexão. As declarações de FK podem não ser aplicadas durante todas as operações da aplicação.

## Logs

São registrados eventos de autenticação e operações relevantes sem incluir senhas ou tokens. Não existe uma trilha de auditoria persistente por alteração.

## Pontos de atenção

- o servidor de `app.py` é somente para desenvolvimento;
- não existe controle de propriedade da ocorrência;
- atualizar uma ocorrência pode substituir seu `usuario_id` pelo usuário que fez a alteração;
- a autorização do campo `status` não é reforçada no endpoint genérico;
- migrações não possuem versão ou rollback.

Veja [[Segurança e Privacidade]] e [[Limitações e Dívida Técnica]].
