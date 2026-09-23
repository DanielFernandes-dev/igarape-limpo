---
tags:
  - produto
  - visão-geral
tipo: conceito
status: atual
---

# Visão Geral

## Problema

Fotografias, coordenadas e observações ambientais isoladas dificultam a comparação de um local ao longo do tempo. Sem um histórico organizado, também é difícil reconhecer recorrência e preparar os dados para análise.

## Proposta

O Igarapé Limpo organiza observações de resíduos como ocorrências georreferenciadas. Cada ocorrência pode ser associada a um ponto monitorado e alimentar:

- mapa interativo;
- histórico do local;
- indicadores e gráficos;
- exportações CSV e GeoJSON.

## Público

- estudantes e pesquisadores;
- projetos de extensão;
- grupos ambientais;
- comunidades interessadas em monitoramento colaborativo.

> [!warning] Limite de finalidade
> O projeto apoia observação e estudo. Ele não substitui órgãos ambientais, serviços de limpeza, fiscalização ou sistemas oficiais.

## Escopo implementado

- autenticação por sessão e três perfis de acesso;
- cadastro e consulta de ocorrências;
- fotografia opcional validada pelo backend;
- pontos monitorados e histórico;
- filtros combináveis no mapa;
- dashboard com indicadores e gráficos;
- exportações CSV e GeoJSON;
- integrações auxiliares no backend;
- testes automatizados do backend e das páginas.

## Fora do escopo atual

- resultados de coleta ambiental formal;
- classificação automática de imagens;
- alertas de tendências;
- operação em alta escala;
- painel visual completo para integrações externas;
- garantias de segurança e disponibilidade de produção.

## Tecnologias principais

| Área | Tecnologia |
|---|---|
| Backend | Python 3 e Flask 3.1 |
| Banco | SQLite |
| Interface | HTML, CSS, JavaScript e Jinja |
| Mapas | Leaflet, OpenStreetMap e MarkerCluster |
| Gráficos | Chart.js |
| Imagens | Pillow |
| Testes | pytest |

## Estado do projeto

| Etapa | Estado |
|---|---|
| Fundamentos e MVP | Concluída |
| Monitoramento | Concluída |
| Gestão e permissões | Concluída no escopo do protótipo |
| Exportação e análise | Concluída |
| Qualidade e segurança básica | Concluída |
| Documentação | Concluída |
| Pesquisa e teste de campo | Próxima |

## Notas relacionadas

- [[Funcionalidades e Fluxos]]
- [[Glossário]]
- [[Roadmap]]
- [[Limitações e Dívida Técnica]]
