---
tags:
  - guia
  - instalação
  - execução
tipo: procedimento
status: atual
---

# Instalação e Execução

## Pré-requisitos

- Python 3;
- acesso à internet para instalar dependências;
- acesso à internet durante o uso completo de mapas, fontes, gráficos e integrações.

## Preparar o ambiente

Execute na raiz do repositório:

```bash
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
```

Dependências diretas:

- Flask 3.1.3;
- Pillow 12.3.0;
- pytest 9.1.1.

## Configurar a sessão

Para manter as sessões válidas após reinícios, defina um segredo persistente:

```bash
export IGARAPE_SECRET_KEY="substitua-por-um-segredo-forte"
```

Quando a aplicação estiver atrás de HTTPS:

```bash
export IGARAPE_HTTPS=1
```

Veja todos os detalhes em [[Configuração]].

## Iniciar

```bash
.venv/bin/python app.py
```

Acesse `http://127.0.0.1:5000`.

Na primeira execução, a aplicação cria:

- `igarape_vivo.db`;
- tabelas e dados seed;
- conta administrativa de desenvolvimento;
- diretório local de uploads, caso necessário.

## Conta de desenvolvimento

```text
E-mail: admin@igarape.local
Senha: admin123
```

> [!danger] Não usar em produção
> Essa credencial é pública e serve somente para desenvolvimento. Ela deve ser substituída antes de qualquer exposição externa.

## Executar os testes

```bash
.venv/bin/pytest -q
```

Os testes usam banco e pasta de uploads temporários. Consulte [[Testes e Qualidade]].

## Arquivos gerados localmente

| Caminho | Conteúdo |
|---|---|
| `igarape_vivo.db` | Banco SQLite local |
| `static/uploads/` | Fotografias enviadas |
| `.venv/` | Ambiente virtual Python |

Esses artefatos não devem ser tratados como documentação nem enviados como resultados de campo.

## Abrir esta documentação no Obsidian

1. Abra o Obsidian.
2. Escolha **Abrir pasta como cofre**.
3. Selecione a pasta `docs/obsidian`.
4. Abra a nota [[00 - Início]].
