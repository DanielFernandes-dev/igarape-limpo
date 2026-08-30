---
tags:
  - testes
  - qualidade
tipo: operacional
status: atual
---

# Testes e Qualidade

## Executar a suíte

Na raiz do projeto:

```bash
.venv/bin/pytest -q
```

## Organização

| Arquivo | Finalidade |
|---|---|
| `tests/conftest.py` | Aplicação, banco e uploads temporários |
| `tests/test_quality.py` | Casos funcionais e de segurança básica |

Os testes substituem o banco e a pasta de uploads por caminhos temporários. A execução não deve alterar `igarape_vivo.db` nem as fotografias locais.

## Cobertura existente

- renderização das páginas principais;
- autenticação válida e inválida;
- proteção da criação de ocorrência;
- filtros por tipo, nível e ponto;
- resumo do dashboard;
- exportações CSV e GeoJSON;
- remoção de `usuario_id` das respostas públicas;
- ocorrência sem fotografia;
- aceitação de PNG válido;
- rejeição de arquivo falso;
- limite de upload com resposta 413;
- headers HTTP de segurança.

## Verificações manuais recomendadas

- login e logout no navegador;
- mapa com e sem acesso à internet;
- geolocalização permitida, negada e indisponível;
- preview e envio de fotografias;
- filtros combinados e exportações sincronizadas;
- dashboard em desktop e celular;
- navegação por teclado;
- foco visível e mensagens de erro;
- comportamento em conexão lenta.

## Lacunas da suíte

- autorização por perfil e por campo;
- propriedade de ocorrência;
- gerenciamento de pontos e usuários;
- integrações externas simuladas;
- migrações e bancos legados;
- JavaScript em navegador real;
- acessibilidade automatizada;
- concorrência e desempenho;
- remoção segura de arquivos após falhas.

## Critério para atualizar esta nota

Não registre uma contagem fixa de testes sem executar a suíte. Ao alterar endpoints, domínios, templates ou contratos DOM, atualize os testes e esta documentação na mesma mudança.

## Relações

- [[Instalação e Execução]]
- [[Segurança e Privacidade]]
- [[Frontend]]
