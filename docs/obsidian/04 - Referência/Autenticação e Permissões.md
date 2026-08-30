---
tags:
  - autenticação
  - autorização
  - segurança
tipo: referência
status: atual
---

# Autenticação e Permissões

## Mecanismo

A autenticação usa sessão Flask armazenada em cookie. Após o login, `usuario_id` é salvo na sessão e carregado em `g.current_user` a cada requisição.

Propriedades do cookie:

- `HttpOnly` habilitado;
- `SameSite=Lax`;
- `Secure` quando `IGARAPE_HTTPS=1`.

As senhas são comparadas com hashes do Werkzeug.

## Perfis

| Perfil | Finalidade |
|---|---|
| `usuario` | Registrar e consultar ocorrências |
| `moderador` | Moderar ocorrências, gerenciar pontos e listar usuários |
| `administrador` | Todas as ações anteriores e criação de usuários |

## Matriz de acesso efetiva

| Operação | Público | Usuário | Moderador | Admin |
|---|:---:|:---:|:---:|:---:|
| Consultar páginas e dados | Sim | Sim | Sim | Sim |
| Exportar ocorrências | Sim | Sim | Sim | Sim |
| Criar ocorrência | Não | Sim | Sim | Sim |
| Atualizar ocorrência | Não | Sim | Sim | Sim |
| Excluir ocorrência | Não | Não | Sim | Sim |
| Criar/alterar ponto | Não | Não | Sim | Sim |
| Listar usuários | Não | Não | Sim | Sim |
| Criar usuário | Não | Não | Não | Sim |

## Diferença entre interface e API

A interface mostra a alteração de status somente para moderadores e administradores. Entretanto, `PUT/PATCH /api/ocorrencias/<id>` aceita atualização de usuário autenticado e não restringe o campo `status` por perfil.

## Propriedade de dados

Não existe regra de propriedade. Um usuário autenticado pode atualizar ocorrências criadas por outra pessoa.

Além disso, o serviço de atualização grava o `usuario_id` de quem altera o registro. Depois de uma edição, esse campo pode representar o último editor, não o autor original.

## Conta inativa

O login verifica se a conta está ativa. A API não expõe uma interface completa para gerenciamento do ciclo de vida das contas.

## Logout

- Página: `POST /logout`, com redirecionamento.
- API: `POST /api/auth/logout`, com resposta JSON.

## Ausências relevantes

- proteção CSRF dedicada;
- recuperação de senha;
- segundo fator;
- expiração e renovação explícitas de sessão por política;
- auditoria persistente;
- autorização por proprietário ou por campo.

## Recomendação antes de produção

Reforçar autorização no serviço, introduzir proteção CSRF, remover a credencial seed, definir política de senhas e registrar autoria e alterações em campos separados.

Veja [[Segurança e Privacidade]] e [[Implantação]].
