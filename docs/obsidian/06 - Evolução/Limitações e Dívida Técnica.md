---
tags:
  - limitações
  - dívida-técnica
tipo: acompanhamento
status: aberto
---

# Limitações e Dívida Técnica

## Produto e metodologia

- não existem resultados de coleta formal;
- critérios visuais ainda não foram calibrados;
- recorrência usa o histórico total, apesar da referência de 90 dias;
- termos de criticidade e recorrência ainda aparecem de forma ambígua;
- não há painel visual completo para integrações;
- não há gestão completa de pontos e usuários na interface.

## Segurança

- ausência de proteção CSRF dedicada;
- usuário autenticado pode atualizar ocorrência alheia;
- campo `status` não possui autorização por perfil no backend;
- atualização substitui a referência de usuário original;
- gateway aceita URL fornecida pelo cliente;
- credencial administrativa seed é conhecida;
- imagens preservam dimensões e metadados;
- não há recuperação de senha, segundo fator ou auditoria persistente.

## Banco e dados

- SQLite limita alta concorrência;
- foreign keys podem não estar ativas em todas as conexões;
- migrações não são versionadas;
- bancos legados podem não receber todos os índices;
- caminhos de banco e upload não são configuráveis por ambiente;
- datas misturam geração UTC e cálculos no horário local do processo;
- não há rotina documentada de backup e restauração.

## API e integrações

- coordenadas inválidas em algumas integrações podem resultar em erro 500;
- `PATCH` não possui semântica confiável para limpar campos opcionais;
- `/api/integracao/status` executa chamadas externas reais;
- a constante do endpoint Nominatim não é usada pelo adaptador;
- endpoints de integração são públicos e não possuem rate limiting;
- o contrato `pontos_criticos` mantém nomenclatura ambígua.

## Frontend e operação

- dependência de CDNs e internet;
- ausência de testes automatizados em navegador;
- acessibilidade não validada com tecnologias assistivas reais;
- servidor atual é somente de desenvolvimento;
- não há container, CI/CD, observabilidade ou configuração de produção;
- uploads locais impedem escalabilidade horizontal direta.

## Testes

- cobertura concentrada em backend e renderização;
- faltam testes de autorização por campo e perfil;
- faltam integrações mockadas;
- faltam testes de migração e banco legado;
- faltam testes de concorrência, desempenho e recuperação.

## Prioridade sugerida

| Prioridade | Tema | Motivo |
|---|---|---|
| Crítica | SSRF, autorização e CSRF | Risco direto antes de exposição pública |
| Alta | Credencial seed, imagens e HTTPS | Proteção de contas e dados |
| Alta | Foreign keys e migrações | Integridade e evolução do banco |
| Média | Terminologia e recorrência | Confiabilidade dos indicadores |
| Média | Testes de navegador e integrações | Redução de regressões |
| Posterior | Escala e PostGIS | Necessário quando houver demanda real |

## Relações

- [[Roadmap]]
- [[Segurança e Privacidade]]
- [[Testes e Qualidade]]
- [[Implantação]]
