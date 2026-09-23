---
tags:
  - roadmap
  - planejamento
tipo: acompanhamento
status: atual
---

# Roadmap

## Estado das fases

| Fase | Entrega | Estado |
|---|---|---|
| 1 | Fundamentos, banco, mapa e CRUD | Concluída |
| 2 | Pontos, histórico, filtros e dashboard | Concluída |
| 3 | Autenticação, perfis e status | Concluída no escopo do protótipo |
| 4 | CSV, GeoJSON e análises | Concluída |
| 5 | Validações, segurança básica e testes | Concluída |
| 6 | Documentação e apresentação | Concluída |
| Pós-fase 6 | Reformulação UX/UI | Concluída |
| 7 | Pesquisa e teste de campo | Próxima |

## Fase 7

- [x] Fundamentar a problemática com fontes sobre os igarapés urbanos de Manaus (relatório técnico, seção 3)
- [ ] Definir área inicial de monitoramento
- [ ] Pesquisar trabalhos e sistemas semelhantes
- [ ] Identificar fontes públicas e geográficas
- [ ] Revisar limitações legais e éticas
- [ ] Validar a [[Metodologia de Campo]]
- [ ] Executar coleta piloto controlada
- [ ] Testar dispositivos, GPS e conexão
- [ ] Avaliar usabilidade e acessibilidade reais
- [ ] Calibrar classificação e recorrência
- [ ] Registrar resultados, falhas e correções

## Antes de exposição pública

- [ ] Corrigir autorização por propriedade e campo
- [ ] Adicionar proteção CSRF
- [ ] Restringir gateway de sensores
- [ ] Remover credencial seed
- [ ] Reprocessar imagens e remover metadados
- [ ] Garantir foreign keys
- [ ] Implantar migrações versionadas
- [ ] Ampliar testes de segurança e integrações

## Evolução operacional

- servidor WSGI e configuração por ambiente;
- backups e restauração testados;
- logs estruturados, métricas e alertas;
- PostgreSQL/PostGIS quando a escala justificar;
- armazenamento de objetos para imagens;
- assets frontend locais ou estratégia resiliente de CDN.

## Trabalhos futuros

### Índice de criticidade

Definir e validar um índice que considere frequência, intensidade e recência, sem reutilizar de forma ambígua o conceito de nível alto.

### Visão computacional

Somente após formar um conjunto de imagens legítimo, autorizado, rotulado e representativo:

- definir classes;
- medir concordância dos rótulos;
- selecionar e avaliar modelos;
- comparar resultado automático e manual;
- documentar limitações e vieses.

### Alertas

Somente após validar tendências em histórico real:

- definir aumento significativo;
- reduzir falsos positivos;
- escolher destinatários e canais;
- registrar confirmação e resolução.

## Regra de escopo

> Registrar → armazenar → localizar → visualizar → analisar.

Funcionalidades avançadas devem vir depois da validação dos dados, da metodologia e da segurança básica.

## Origem detalhada

O histórico completo de tarefas e sessões permanece no arquivo `TODO.MD` da raiz do projeto.
