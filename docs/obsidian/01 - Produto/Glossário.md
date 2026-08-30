---
tags:
  - produto
  - glossário
tipo: referência
status: atual
---

# Glossário

## Ocorrência

Registro de uma observação ambiental com coordenadas, data, tipo de resíduo, nível de acúmulo, status e informações opcionais.

## Ponto monitorado

Referência geográfica estável à qual várias ocorrências podem ser associadas para formar um histórico.

## Nível de acúmulo

- `Baixo`: poucos itens isolados, sem bloqueio visível.
- `Medio`: concentração perceptível e localizada.
- `Alto`: grande concentração, espalhamento relevante ou possível obstrução.

Os níveis são estimativas visuais do protótipo e ainda precisam de validação em campo.

## Tipo de resíduo

| Valor interno | Interpretação |
|---|---|
| `Plastico` | Garrafas, sacolas e embalagens plásticas |
| `Metal` | Latas, peças e sucata metálica |
| `Vidro` | Garrafas, frascos e fragmentos |
| `Organico` | Restos vegetais ou alimentares |
| `Papel` | Papel, papelão e semelhantes |
| `Misto` | Categorias combinadas sem predominância clara |
| `Outro` | Material fora das categorias anteriores |

## Status da ocorrência

Estado operacional: `Nova`, `Em analise`, `Em atendimento`, `Resolvida` ou `Descartada`.

Status não é o mesmo que nível de acúmulo. O nível descreve a observação; o status descreve seu acompanhamento.

## Ponto recorrente

Ponto com pelo menos três ocorrências no histórico total. A regra atual não aplica uma janela temporal.

## Ocorrência de nível alto

Ocorrência cujo `nivel_acumulo` é `Alto`. No filtro atual do mapa, a expressão visual “pontos críticos” corresponde a essas ocorrências, mesmo que elas não estejam associadas a um ponto recorrente.

## `pontos_criticos`

Nome mantido no contrato JSON do dashboard para a contagem de pontos recorrentes. O nome é legado e não significa necessariamente ocorrências de nível alto.

> [!important] Distinção essencial
> **Nível alto** é uma classificação da ocorrência. **Recorrência** é uma contagem histórica do ponto. O campo **`pontos_criticos`** é atualmente usado pelo backend para representar pontos recorrentes.

## Seed

Dados automáticos de exemplo criados na primeira inicialização. Não representam resultados ambientais reais.

## Gateway de sensores

Serviço HTTP externo que retorna dados de sensores em JSON. No protótipo, a URL e o token são recebidos do cliente.

## Notas relacionadas

- [[Modelo de Dados]]
- [[Metodologia de Campo]]
- [[Limitações e Dívida Técnica]]
