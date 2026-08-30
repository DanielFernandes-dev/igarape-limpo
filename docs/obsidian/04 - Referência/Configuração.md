---
tags:
  - configuração
  - ambiente
tipo: referência
status: atual
---

# Configuração

## Variáveis de ambiente

| Variável | Obrigatória | Efeito |
|---|---|---|
| `IGARAPE_SECRET_KEY` | Recomendada | Segredo persistente da sessão Flask |
| `IGARAPE_HTTPS` | Não | Quando igual a `1`, ativa `Secure` no cookie |

Exemplo de desenvolvimento:

```bash
export IGARAPE_SECRET_KEY="um-segredo-local-forte"
.venv/bin/python app.py
```

> [!warning] Chave aleatória
> Sem `IGARAPE_SECRET_KEY`, uma nova chave aleatória é gerada ao iniciar o processo. Sessões existentes deixam de ser válidas após o reinício.

O projeto não carrega automaticamente arquivos `.env` e não depende de `python-dotenv`.

## Caminhos locais

| Configuração | Valor padrão |
|---|---|
| Banco | `igarape_vivo.db` |
| Schema | `schema.sql` |
| Uploads | `static/uploads` |

Esses caminhos derivam da raiz do repositório e não são configuráveis por variável de ambiente na implementação atual.

## Uploads

- extensões: PNG, JPG, JPEG, GIF e WebP;
- limite total: 10 MiB por requisição;
- nomes internos: UUID;
- validação de conteúdo: Pillow.

## Domínios

`config.py` define:

- tipos de resíduo;
- níveis de acúmulo;
- status de ocorrência;
- status de ponto;
- cores dos níveis.

Consulte [[Glossário]] para a interpretação funcional.

## Localização padrão

- centro: Manaus;
- latitude: `-3.1190`;
- longitude: `-60.0217`;
- zoom: `12`;
- timezone declarado: `America/Manaus`.

O bounding box de hidrografia também cobre uma região predefinida de Manaus.

## Serviços externos

`config.py` contém endpoints para Overpass, Open-Meteo e Nominatim. O adaptador Nominatim usa atualmente uma URL literal em vez da constante `NOMINATIM_ENDPOINT`.

## Ambientes

Não existem classes separadas para desenvolvimento, teste e produção. Os testes substituem caminhos de banco e uploads com `monkeypatch`.

Também não existem Dockerfile, Compose, configuração WSGI ou proxy reverso no repositório.

## Arquivo de referência

Todas as configurações descritas estão em `config.py`, exceto substituições temporárias usadas pelos testes.
