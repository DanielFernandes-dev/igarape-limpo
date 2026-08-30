---
tags:
  - guia
  - apresentação
tipo: roteiro
status: atual
---

# Apresentação e Demonstração

## Objetivo

Apresentar em aproximadamente dez minutos o problema, a proposta, o protótipo, os resultados técnicos, as limitações e os próximos passos.

## Sequência sugerida

1. Explique a dispersão de fotografias e coordenadas ambientais.
2. Apresente a proposta de histórico georreferenciado.
3. Resuma a [[Visão Arquitetural]].
4. Faça login.
5. Registre uma ocorrência de demonstração.
6. Aplique filtros no mapa.
7. Abra o detalhe e o histórico de um ponto.
8. Apresente o dashboard.
9. Exporte CSV e GeoJSON.
10. Diferencie resultados técnicos de resultados ambientais.

## Preparação

```bash
.venv/bin/pytest -q
.venv/bin/python app.py
```

Antes da apresentação:

- confirme o acesso a `http://127.0.0.1:5000`;
- teste login e logout;
- confirme mapa, gráficos e acesso à internet;
- use uma ocorrência sem dados pessoais;
- valide as exportações;
- teste uma largura de tela móvel;
- prepare capturas de contingência.

## Pontos para destacar

- arquitetura em camadas;
- associação entre ocorrência e ponto monitorado;
- filtros e exportações sincronizados;
- validação de conteúdo de imagem com Pillow;
- interface responsiva e recursos de acessibilidade;
- testes isolados do banco local.

## Comunicação responsável

> [!important] Resultados técnicos
> É correto afirmar que o protótipo possui cadastro, consulta, filtros, histórico, dashboard, exportações e testes automatizados.

> [!warning] Resultados ambientais
> Ainda não houve coleta formal. Não use registros seed como evidência de poluição, recorrência real ou eficácia ambiental.

## Plano sem internet

- demonstre páginas e API locais;
- use capturas previamente preparadas para mapas e gráficos;
- explique a dependência atual de CDNs e serviços externos;
- mostre que os dados locais permanecem no SQLite.

## Encerramento sugerido

> O Igarapé Vivo transforma observações ambientais em dados georreferenciados que podem ser visualizados, comparados e acompanhados ao longo do tempo, sem substituir os órgãos responsáveis.

## Depois da apresentação

Encerre o servidor e descarte qualquer dado de demonstração que contenha informação indevida.
