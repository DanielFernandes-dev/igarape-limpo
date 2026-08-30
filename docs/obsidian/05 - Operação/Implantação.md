---
tags:
  - implantação
  - produção
  - operação
tipo: operacional
status: protótipo
---

# Implantação

## Estado atual

`app.py` inicia o servidor de desenvolvimento Flask com debug habilitado. Esse processo não é apropriado para produção.

Não existem no repositório:

- servidor WSGI configurado;
- Dockerfile ou Compose;
- proxy reverso;
- pipeline de implantação;
- observabilidade estruturada;
- política de backup;
- configuração separada por ambiente.

## Execução local

```bash
export IGARAPE_SECRET_KEY="segredo-local"
.venv/bin/python app.py
```

Consulte [[Instalação e Execução]].

## Requisitos mínimos para produção

### Aplicação

- usar um servidor WSGI de produção;
- desativar debug;
- separar configurações de desenvolvimento e produção;
- definir timeouts e limites de processo;
- criar endpoint de saúde que não dependa de terceiros.

### Segurança

- definir `IGARAPE_SECRET_KEY` persistente;
- servir somente por HTTPS;
- definir `IGARAPE_HTTPS=1`;
- trocar a conta seed;
- corrigir os itens de [[Segurança e Privacidade]].

### Dados

- avaliar PostgreSQL/PostGIS para concorrência e consultas geográficas;
- usar armazenamento de objetos para imagens;
- implementar migrações versionadas;
- automatizar backups e testar restauração;
- definir retenção e exclusão.

### Rede e integrações

- configurar endpoints e credenciais no servidor;
- bloquear URLs arbitrárias do gateway;
- aplicar allowlist e restrições de saída;
- monitorar latência, erros e limites dos provedores;
- avaliar cache respeitando os termos de uso.

### Observabilidade

- logs estruturados com correlação de requisições;
- métricas de latência, erros e uso de recursos;
- alertas operacionais;
- trilha de auditoria separada dos logs técnicos.

## Assets do frontend

Leaflet, MarkerCluster, Chart.js e fontes são carregados por CDN. Para operação resiliente, avalie versionar os assets localmente e aplicar uma política de segurança de conteúdo adequada.

## Checklist de liberação

- [ ] Testes automatizados aprovados
- [ ] Debug desativado
- [ ] Segredo persistente configurado
- [ ] HTTPS e cookie `Secure` ativos
- [ ] Credencial seed removida ou substituída
- [ ] Autorização e CSRF corrigidos
- [ ] Gateway externo restrito
- [ ] Migrações e backup testados
- [ ] Fotografias reprocessadas sem metadados
- [ ] Logs, métricas e alertas configurados
- [ ] Política de privacidade e retenção aprovada
- [ ] Teste de restauração concluído

## Escalabilidade

SQLite e uploads locais são adequados para demonstração com baixa concorrência. Múltiplas instâncias exigem banco compartilhado, armazenamento de objetos e coordenação de sessões.
