---
tags:
  - segurança
  - privacidade
tipo: operacional
status: atenção
---

# Segurança e Privacidade

## Controles implementados

- hash de senha com Werkzeug;
- cookie de sessão `HttpOnly` e `SameSite=Lax`;
- opção `Secure` por `IGARAPE_HTTPS=1`;
- segredo configurável por `IGARAPE_SECRET_KEY`;
- consultas SQL parametrizadas;
- validação de coordenadas, domínios e tamanhos;
- limite de 10 MiB por requisição;
- validação de extensão e conteúdo de imagens;
- nomes UUID para uploads;
- remoção de hash e identificador de usuário das respostas públicas;
- headers contra MIME sniffing e framing;
- política de referência;
- erro interno genérico na API;
- logs sem senha ou token.

## Riscos conhecidos

### Autorização insuficiente

Qualquer usuário autenticado pode atualizar qualquer ocorrência. O campo `status` também não possui autorização por perfil no endpoint genérico.

### Gateway e SSRF

Os endpoints públicos de sensores aceitam uma URL fornecida pelo cliente e fazem a requisição no servidor. Isso pode permitir acesso indevido a serviços internos.

### CSRF

A aplicação usa autenticação por cookie e não possui proteção CSRF dedicada para operações de escrita.

### Credencial seed

A conta `admin@igarape.local` com senha conhecida é criada para desenvolvimento. Ela não pode permanecer em uma implantação pública.

### Fotografias

Pillow valida o formato, mas as imagens não são redimensionadas, reprocessadas ou limpas de metadados. Informações EXIF podem permanecer.

### Sessões

Sem segredo persistente, as sessões são invalidadas a cada reinício. Sem HTTPS e `IGARAPE_HTTPS=1`, o cookie não recebe a flag `Secure`.

### Integridade do banco

As chaves estrangeiras podem não estar ativas em todas as conexões SQLite. Isso pode permitir referências órfãs.

## Privacidade na coleta

- evite rostos, placas e documentos;
- registre somente observações ambientais necessárias;
- não inclua dados pessoais nas observações;
- informe participantes sobre finalidade e retenção;
- limite a precisão pública da localização quando houver risco;
- defina política de exclusão de imagens e registros;
- valide exigências legais e éticas antes da coleta formal.

## Antes de produção

1. Corrigir autorização por perfil, campo e propriedade.
2. Adicionar proteção CSRF.
3. Remover ou trocar a credencial seed.
4. Configurar segredo persistente e HTTPS.
5. Restringir integrações com allowlist e configuração no servidor.
6. Remover metadados e gerar imagens otimizadas.
7. Adicionar recuperação segura de acesso e política de credenciais.
8. Criar auditoria persistente.
9. Garantir foreign keys e migrações versionadas.
10. Definir retenção, backup e resposta a incidentes.

## Modelo de ameaça mínimo

| Ativo | Ameaça | Controle necessário |
|---|---|---|
| Contas | Roubo de sessão/senha | HTTPS, política de acesso, expiração |
| Ocorrências | Alteração indevida | Propriedade e autorização por campo |
| Fotografias | Exposição de dados pessoais | Reprocessamento, retenção e acesso |
| Servidor | SSRF por gateway | Allowlist e bloqueio de redes internas |
| Banco | Corrupção ou perda | FK, migrações e backups testados |

## Relações

- [[Autenticação e Permissões]]
- [[Integrações Externas]]
- [[Implantação]]
- [[Metodologia de Campo]]
