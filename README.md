# Igarapé Limpo

Sistema colaborativo para registrar, localizar, acompanhar e analisar ocorrências de resíduos sólidos em corpos d'água urbanos.

## Equipe

- Daniel Fernandes de Oliveira da Silva
- Adriano Alves Barros
- Carlos Johnatan Silva Souza Rodrigues
- Julio Thiago Colares de Lima

## Estado atual

As **Fases 1 a 6 estão concluídas**:

| Fase | Entrega | Status |
|---|---|---|
| 1 — Fundamentos | MVP, banco, mapa e API CRUD | Concluída |
| 2 — Monitoramento | Pontos, histórico, filtros e dashboard | Concluída |
| 3 — Gestão | Autenticação, perfis, permissões e status | Concluída |
| 4 — Dados | CSV, GeoJSON e análises | Concluída |
| 5 — Qualidade | Segurança, validações e testes | Concluída |
| 6 — Documentação | Documentação técnica e apresentação | Concluída |
| 7 — Pesquisa e campo | Metodologia e coleta em ambiente real | Próxima |

A interface também recebeu uma reformulação UX/UI posterior à Fase 6, com identidade visual temática, responsividade, acessibilidade e feedbacks de interação.

## Problema e objetivo

Fotografias, coordenadas e observações ambientais isoladas dificultam a comparação de um mesmo local ao longo do tempo. O Igarapé Limpo organiza essas observações como dados georreferenciados e históricos.

O projeto não substitui órgãos ambientais, equipes de limpeza ou sistemas oficiais. Seu objetivo é oferecer uma ferramenta de apoio para estudantes, pesquisadores, projetos de extensão, grupos ambientais e comunidades.

Fluxo central:

> registrar → validar → localizar → visualizar → analisar → acompanhar → comparar → exportar

## Funcionalidades implementadas

### Registro e gestão

- Login, logout e sessão autenticada.
- Perfis `usuario`, `moderador` e `administrador`.
- Cadastro de ocorrência com coordenadas, tipo, nível, fotografia e observações.
- Localização pelo navegador, seleção no mapa ou ponto monitorado.
- Associação opcional da ocorrência a um ponto monitorado.
- Status: `Nova`, `Em analise`, `Em atendimento`, `Resolvida` e `Descartada`.
- CRUD de ocorrências e gestão de pontos conforme permissão.

### Mapa e monitoramento

- Leaflet com base OpenStreetMap.
- Marcadores por nível de acúmulo e agrupamento com MarkerCluster.
- Filtros combináveis por tipo, nível, ponto, período e texto.
- Exibição somente de ocorrências de nível alto.
- Popups, centralização, lista recente e exportações sincronizadas com os filtros.
- Página de ponto monitorado com mapa, resumo, distribuições, recorrência e histórico.

### Dashboard e dados

- Totais gerais e ocorrências nos últimos 7 e 30 dias.
- Pontos ativos e recorrentes.
- Resíduo e local mais frequentes.
- Gráficos por tipo, nível, evolução temporal e ranking de pontos.
- Exportação CSV e GeoJSON, inclusive com filtros.

### Segurança e qualidade

- Senhas armazenadas com hash do Werkzeug.
- Cookies `HttpOnly`, `SameSite=Lax` e opção `Secure` por ambiente.
- Headers `X-Content-Type-Options`, `X-Frame-Options` e `Referrer-Policy`.
- Validação de coordenadas, domínios e tamanho de campos.
- Validação de extensão e conteúdo real de imagens com Pillow.
- Limite de 10 MB por requisição.
- Respostas públicas sem `senha_hash` ou `usuario_id`.
- Logs de autenticação e operações sem dados sensíveis.
- Resposta genérica para erros internos da API.
- 20 testes automatizados com banco e uploads temporários.

## Experiência e interface

A camada visual combina `static/css/style.css` com a reformulação em `static/css/ui.css`.

- Paleta inspirada em floresta, água, argila e areia.
- Tipografia Lora e Manrope, com fallbacks locais.
- Cabeçalho fixo, navegação ativa e área de conta.
- Layouts específicos para mapa, dashboard, formulário, login, detalhes e histórico.
- Breakpoints para desktop, tablet e celular.
- Preview da fotografia antes do envio.
- Botões bloqueados durante requisições e mensagens contextuais.
- Estados vazios e falhas de rede apresentados ao usuário.
- Skip link, foco visível, regiões ARIA, `aria-live` e suporte a `prefers-reduced-motion`.

## Critérios atuais

Tipos de resíduo:

`Plastico`, `Metal`, `Vidro`, `Organico`, `Papel`, `Misto`, `Outro`.

Níveis de acúmulo:

- `Baixo`: itens isolados, sem bloqueio visível.
- `Medio`: concentração perceptível e localizada.
- `Alto`: grande concentração ou possível obstrução.

Esses níveis são estimativas visuais do protótipo e ainda precisam de validação na Fase 7.

Um ponto é considerado recorrente quando possui ao menos três ocorrências no histórico total. No mapa, o filtro de criticidade representa ocorrências classificadas como nível `Alto`.

## Tecnologias

- Python 3 + Flask 3.1.
- SQLite.
- HTML, CSS, JavaScript e templates Jinja.
- Leaflet, OpenStreetMap e Leaflet.markercluster.
- Chart.js.
- Pillow para validação de imagens.
- pytest para testes automatizados.
- Integrações auxiliares: Overpass, Open-Meteo, Nominatim e gateway JSON de sensores.

## Estrutura

```text
igarape-limpo/
├── app.py
├── config.py
├── database.py
├── schema.sql
├── app/
│   ├── __init__.py
│   ├── routes/
│   ├── services/
│   ├── repositories/
│   ├── integrations/
│   └── utils/
├── templates/
├── static/
│   ├── css/
│   ├── js/
│   └── uploads/
├── tests/
├── docs/
│   └── obsidian/                 # documentação técnica navegável
├── ARQUITETURA.md
├── APRESENTACAO.md
├── RELATORIO.md
└── TODO.MD
```

## Instalação e execução

```bash
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
.venv/bin/python app.py
```

Acesse `http://127.0.0.1:5000`.

Na primeira execução, o banco e os dados seed são criados automaticamente. As imagens ficam em `static/uploads/`.

Conta seed de desenvolvimento:

```text
E-mail: admin@igarape.local
Senha: admin123
```

Essa credencial deve ser substituída antes de qualquer exposição externa. Configure `IGARAPE_SECRET_KEY` e use `IGARAPE_HTTPS=1` quando a aplicação estiver atrás de HTTPS.

## Testes

```bash
.venv/bin/pytest -q
```

Resultado consolidado atual: **20 testes aprovados**. A suíte cobre páginas, autenticação, proteção de rotas, filtros, dashboard, exportações, privacidade, imagens, limite de upload e headers de segurança.

## Integrações externas

O backend possui adaptadores e endpoints para:

- hidrografia via Overpass/OpenStreetMap;
- meteorologia via Open-Meteo;
- geocodificação reversa via Nominatim;
- gateway JSON de sensores e exportação CSV.

Esses adaptadores ainda não formam um painel visual completo. O gateway recebe URL e token do cliente no protótipo e precisa de configuração no servidor e allowlist antes de produção.

## Limitações

- Não há resultados ambientais de coleta formal; os registros atuais são seed e testes.
- SQLite e armazenamento local de imagens não atendem alta concorrência.
- Não há migrações versionadas, recuperação de senha ou proteção CSRF dedicada.
- Um usuário autenticado ainda pode atualizar ocorrências que não criou.
- Fotografias não são redimensionadas e seus metadados não são removidos.
- Mapa, fontes, gráficos e integrações externas dependem de internet.
- Critérios de recorrência e criticidade ainda são simplificados.

## Próxima fase

A Fase 7 depende de decisões e atividades fora do código. A primeira etapa da fundamentação documental (fontes jornalísticas e institucionais sobre a situação dos igarapés urbanos de Manaus) já foi incorporada à seção 3 do relatório técnico; a pesquisa de campo e a fundamentação com artigos científicos permanecem pendentes.

1. definir a área inicial e fontes de dados;
2. validar metodologia e critérios;
3. executar coleta controlada;
4. testar dispositivos, conexão, localização e fotografia em campo;
5. registrar resultados, problemas de usabilidade e correções.

Visão computacional e alertas permanecem como trabalhos futuros, posteriores à formação de um histórico confiável.

## Documentos

- [`docs/obsidian/00 - Início.md`](docs/obsidian/00%20-%20In%C3%ADcio.md): base de conhecimento navegável para abrir como cofre no Obsidian.
- `ARQUITETURA.md`: componentes, fluxos, segurança e implantação.
- `APRESENTACAO.md`: roteiro de apresentação e demonstração.
- `TODO.MD`: painel de fases e histórico de progresso.
- [`RELATORIO.md`](RELATORIO.md): relatório técnico do projeto em norma ABNT, com integrantes, fundamentação da problemática a partir de fontes sobre a situação dos igarapés urbanos de Manaus (seção 3) e as pendências do backlog (pesquisa de campo, coleta de fotografias, fundamentação com artigos científicos e testes em campo).
