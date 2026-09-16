# Design: Login × Mapa — estrutura e gaps funcionais

> Documento de apoio para alinhar a estrutura visual/funcional da página do mapa (`templates/index.html`) à estrutura de design já consolidada do login (`templates/login.html`).
>
> Arquivos de referência: `templates/login.html`, `templates/index.html`, `templates/base.html`, `static/css/ui.css`, `static/js/map.js`, `app/routes/pages.py`, `app/routes/api.py`.

---

## 1. Estrutura do Login

### 1.1 Template — `templates/login.html`

- Estende `base.html` (herda header `.topo`, nav, footer `.rodape`).
- Bloco `conteudo` → estrutura:

```
<div class="auth-container">          → container centralizado (max 880px, margem vertical)
  <div class="auth-shell">            → "casca": grid 2 colunas, cantos 24px, sombra, borda
    <section class="auth-contexto">   → painel contextual escuro (--floresta-900)
        🇪🇬 eyebrow "Área de gestão"
        h1 "Dados ambientais com contexto."
        p  convite/descrição
    </section>
    <form id="form-login" class="form auth-form">   → painel claro (branco)
        eyebrow "Acesso seguro"
        h2 "Entrar na plataforma"
        .campo (label + input email)
        .campo (label + input senha)
        .btn.btn-primario "Entrar"
        #msg-login (role="status" aria-live="polite")
        .auth-nota (texto de rodapé do formulário)
    </form>
  </div>
</div>
```

- Bloco `scripts`: JS inline faz `fetch POST /api/auth/login` (`fetch` com JSON `{email, senha}`), feedback de loading no botão (`Entrando...`), mensagens `.msg.ok`/`.msg.erro`, redirect para `/` em sucesso.

### 1.2 CSS — `static/css/ui.css`

| Seletor | Papel | Posicionamento |
|---|---|---|
| `.auth-container` | Contém e centraliza | `max-width: 880px; margin: 2rem auto;` |
| `.auth-shell` | Casca 2 colunas | `grid-template-columns: .95fr 1.05fr; border-radius: 24px; box-shadow: var(--sombra); border; overflow: hidden;` |
| `.auth-contexto` | Painel narrativo escuro | `background: var(--floresta-900); color: #e8f2ee; padding: 3rem 2.5rem;` + `::after` círculo decorativo |
| `.auth-form` | Formulário branco puro | `border: 0; border-radius: 0; box-shadow: none; padding: 3rem 2.5rem;` |
| `.auth-nota` | Aviso discreto | `font-size: .72rem; color: var(--tinta-suave);` |

- Responsivo: `@media (max-width: 700px)` → `.auth-shell { grid-template-columns: 1fr; }`; painéis com padding reduzido (2rem).

### 1.3 Backend envolvido

- Rota GET: `pages.login` em `app/routes/pages.py:42` — redireciona para `/` se já autenticado (`session.get("usuario_id")`).
- API POST: `/api/auth/login` em `app/routes/api.py:35` — valida e-mail/senha, chama `auth_service.autenticar`, grava `session["usuario_id"]`, retorna `{"usuario": ...}`.
- Sessão: carregada em `app/__init__.py` (`before_request`), exposta ao template via `current_user`.

---

## 2. Estrutura da página do Mapa

### 2.1 Template — `templates/index.html`

- Estende `base.html`; bloco `styles` carrega CSS do MarkerCluster; bloco `scripts` carrega Leaflet 1.9.4 + MarkerCluster 1.5.3 + `static/js/map.js`.

```
<header class="page-header">                 → cabeçalho da página
  .page-header-copy                          → eyebrow + h1 + .page-intro
  .page-actions                              → btn "Registrar ocorrência"
</header>

<section class="filtros">                    → painel de filtros
  .filtros-titulo "Refinar visualização"
  form#form-filtros.form-filtros
    .filtro-grupo (tipo resíduo)            select
    .filtro-grupo (nível acúmulo)           select
    .filtro-grupo (ponto monitorado)        select
    .filtro-grupo (data inicial)            input[date]
    .filtro-grupo (data final)              input[date]
    .filtro-grupo-busca                     input[search]
    .filtro-check "Apenas nível alto"       checkbox
    .filtro-acoes                           btns "Aplicar filtros" / "Limpar"
</section>

<section class="cards">                     → 4 KPIs
  4× .card (.card-valor + .card-rotulo + .card-nota)
</section>

<section class="mapa-card">                 → o mapa
  .painel-cabecalho (h2 + #resultado-filtros aria-live)
  #mapa (role="region")                     → contêiner Leaflet (520px)
  .mapa-rodape
    .legenda (Baixo/Médio/Alto) + .exportacoes (CSV / GeoJSON)
</section>

<section id="lista-recente" class="lista-card">  → registros recentes
  .painel-cabecalho
  ul#lista
</section>
```

### 2.2 CSS — `static/css/ui.css` (seções do mapa)

| Seletor | Papel |
|---|---|
| `.page-header` | Grid `1fr auto` (título + ação) |
| `.filtros` | Painel branco padrão (`background rgba(255,255,255,.88)`, borda, `var(--raio)`, sombra) |
| `.form-filtros` / `.filtro-grupo` | Campos em linha flexível |
| `.cards` / `.card` | Grade de 4 KPIs com detalhes decorativos (`::after`) |
| `.mapa-card` | Painel que "envolve" o mapa (`overflow: hidden; padding: .75rem`) |
| `#mapa` | `height: 520px; border-radius: 13px` |
| `.mapa-rodape` | Legenda + exportações |
| `.lista-card` | Painel de lista recente |

### 2.3 JS — `static/js/map.js`

- Inicializa `L.map("mapa")` centrado em Manaus ≈ `[-3.059860, -60.040980]`, zoom 13, zoom control bottomright.
- Tile: OpenStreetMap; cluster com `maxClusterRadius: 48`.
- `carregarOcorrencias()` → GET `/api/ocorrencias` com filtros; atualiza exportações, `renderizarOcorrencias`, `renderizarResumo` (4 KPIs), `renderizarLista`.
- Popups com detalhe + link "Ver detalhes"/"Histórico do ponto".

---

## 3. Design e gaps funcionais (Login × Mapa)

### 3.1 O que o login acerta

1. **Âncora visual única**: todo o conteúdo fica dentro de uma casca `.auth-shell` (1 card, 2 painéis) — hierarquia clara, sem rolagem longa.
2. **Narrativa contexto → ação**: painel escuro conta "por quê" (`.auth-contexto`), painel claro executa (`.auth-form`). Padrão editorial forte.
3. **Estética diferenciada**: canto de 24px + `var(--sombra)` (a mais forte do tema) + círculo decorativo `::after` — diferencia a página das demais do sistema.
4. **Micro-interação**: estados de loading no botão (`Entrando...`) e mensagens `role="status"` com `aria-live`.
5. **Padrão tipográfico**: `eyebrow` + `h1`/`h2` definem dois níveis de leitura (marca/contextual e funcional).

### 3.2 Gaps funcionais do Mapa em relação ao Login

| # | Gap | Descrição |
|---|---|---|
| G1 | **Sem casca/âncora** | O mapa usa `max-width: 1240px` em colunas soltas (header, filtros, cards, mapa, lista). Falta um "shell" que una a experiência como o `auth-shell` faz no login. |
| G2 | **Filtros fora de contexto** | Os filtros abrem a página antes do mapa — o usuário "trabalha" antes de ver o dado principal. No login, o contexto vem antes do formulário (`.auth-contexto` → `.auth-form`). |
| G3 | **Hierarquia visual diferente** | Login tem painel escuro temático (`--floresta-900`); a página do mapa fica quase toda clara/branca, perdendo a identidade "ambiental" do tema. |
| G4 | **Sobrecarga de rolagem** | Header + filtros + 4 cards + mapa 520px + lista = página longa; no login tudo cabe em uma viewport (880px). |
| G5 | **Feedback assíncrono desigual** | O login tem loading explícito no botão e mensagens `.msg` com `aria-live`; o mapa troca texto do botão (`Atualizando...`) e do `#resultado-filtros`, mas sem painel de erro/empty destacado (faltam estados visuais de vazio/carregamento/erro como no `.msg`). |
| G6 | **Responsividade do mapa** | Em telas pequenas, a pilha filtros → cards → mapa deixa o mapa longe da rolagem inicial (linha 260: `#mapa` height min 62vh). O `auth-shell` colapsa elegantemente para 1 coluna; o mapa espalha 5 blocos. |
| G7 | **Botões de ação dispersos** | Login concentra 1 ação (`Entrar`). O mapa espalha ações (Registrar, Aplicar filtros, Limpar, CSV, GeoJSON) por 4 pontos da página — sem um agrupamento padrão "shell". |
| G8 | **Sem painel editorial** | Faltam os elementos de storytelling do login (eyebrow contextual, nota de rodapé da seção) para explicar o que o mapa está mostrando. |

---

## 4. Mudanças propostas — adequar o Mapa ao design do Login

Estratégia geral: **repetir o padrão "contexto + painel(s)" do `auth-shell` na página do mapa**, reutilizando tokens e classes do `ui.css` para não duplicar CSS.

### 4.1 Criar uma casca unificada (.plataforma-shell)

Espelhar `.auth-shell` em `templates/index.html`:

```
<div class="plataforma-container">      → análogo a .auth-container
  <div class="plataforma-shell">        → análogo a .auth-shell (grid 2 col, 24px, sombra)
    ...blocos atuais...
  </div>
</div>
```

CSS novo em `ui.css` (reusando tokens existentes):

```css
.plataforma-container { max-width: 1240px; margin: 1.25rem auto; }
.plataforma-shell {
    display: grid; grid-template-columns: minmax(0, 1fr);
    overflow: hidden; border-radius: var(--raio);
    box-shadow: var(--sombra); border: 1px solid var(--linha);
    background: rgba(255,255,255,.9);
}
.plataforma-shell .plataforma-col {
    display: grid; gap: 1.1rem; padding: clamp(1.25rem, 3vw, 2rem);
}
```

### 4.2 Painel contextual escuro no topo do mapa (espelho de .auth-contexto)

- Adicionar um header interno da casca (mesmo tratamento de `.auth-contexto`: `background: var(--floresta-900)`, eyebrow, h1 branco, texto `#b9d0c8`, círculo decorativo `::after`).

```css
.plataforma-contexto {
    position: relative; overflow: hidden; padding: clamp(1.75rem, 4vw, 3rem) clamp(1.5rem, 4vw, 2.5rem);
    color: #e8f2ee; background: var(--floresta-900);
}
.plataforma-contexto::after { /* mesmo círculo decorativo do auth-contexto */ }
.plataforma-contexto h1 { color: white; }
.plataforma-contexto p { color: #b9d0c8; }
```

- Mover (ou duplicar estilizado) o `header.page-header` para dentro do `.plataforma-contexto`, mantendo o `.page-actions` como `justify-content: flex-start`.

### 4.3 Estrutura em 2 colunas (contexto lateral ↔ conteúdo)

Espelhar a proporção `.95fr 1.05fr` do login:

```
.plataforma-shell { grid-template-columns: minmax(0, 1fr) minmax(360px, .42fr); }

Coluna principal (mapa)                 Coluna lateral (painéis "form-like")
──────────────────────────────          ──────────────────────────────
.mapa-card (mapa + legenda + exports)   .filtros (filtros refinados)
.lista-card (ocorrências recentes)      .cards (4 KPIs compactos)
```

- Filtros passam a ter a cara de `.auth-form`: painel branco puro, `border: 0`, rótulos `.campo label` (link G2: contexto antes do trabalho).
- KPIs condensados (indicadores de recorte) na lateral, como um resumo "de apoio" — equivalente ao `.auth-contexto`/`.auth-nota` que contextualiza.

### 4.4 Feedback visual uniforme (fecha G5)

- Adotar o padrão `.msg` do login em `index.html`:
  - `<p id="msg-mapa" class="msg" role="status" aria-live="polite"></p>` dentro do `.mapa-card`.
  - Em `map.js`, trocar `status.textContent = ...` por `status.textContent = ...; status.className = "msg"` / `"msg ok"` / `"msg erro"`, e reutilizar `.msg.ok` / `.msg.erro` já existentes no `ui.css`.
  - Estado vazio da lista já usa `.estado-vazio` — padronizar o texto dentro do `.msg-mapa`.

### 4.5 Ações agrupadas e consistentes (fecha G7)

- Exportações (CSV/GeoJSON) como `.btn-exportar` compactos no `.mapa-rodape` (já é assim).
- Mover "Registrar ocorrência" para o `.plataforma-contexto` com `.btn-claro` (tom sobre fundo escuro, como o login concentra a ação). "Aplicar filtros"/"Limpar" permanecem na lateral, mas com os mesmos padrões `.btn` do login.

### 4.6 Responsividade (fecha G6) — espelho do @700px do login

```css
@media (max-width: 900px) {
    .plataforma-shell { grid-template-columns: 1fr; }
    .filtros, .cards, .mapa-card, .lista-card { grid-column: auto; }
}
@media (max-width: 700px) {
    .plataforma-contexto { padding: 2rem 1.5rem; }   /* mesmo recuo do .auth-contexto */
    .mapa-card, .filtros, .cards, .lista-card { border-radius: var(--raio-menor); }
}
```

### 4.7 Consistência de tokens (fecha G3)

- Unificar os painéis `.filtros`, `.mapa-card`, `.lista-card` para o mesmo "look" da casca (borda `var(--linha)`, `var(--raio)`, sombra suave) e remover o `rgba(255,255,255,.88)` individual em favor do fundo da `.plataforma-shell`.
- Reaproveitar `var(--sombra)` (a sombra do login) na `.plataforma-shell` para dar peso visual à página.

---

## 5. Resumo da entrega

| Item | Login (fonte) | Mapa (hoje) | Mapa (proposto) |
|---|---|---|---|
| Casca de página | `.auth-shell` grid 2 col | blocos soltos em 1240px | `.plataforma-shell` grid `1fr .42fr` |
| Painel contextual | `.auth-contexto` escuro | `header.page-header` claro | `.plataforma-contexto` escuro (eyebrow + h1) |
| Formulário/painel | `.auth-form` branco puro | `.filtros` cinza translúcido | espelho de `.auth-form` na lateral |
| Feedback | `.msg` + `role="status"` | `status.textContent` apenas | `.msg-mapa` ok/erro + aria-live |
| Ação principal | 1 botão no form | 4 pontos de ação | principal no contexto escuro, resto agrupado |
| Responsivo | 1 coluna @700px | pilha longa | 1 coluna @900px com recuos iguais ao login |

### Verificação sugerida

- Rodar a suíte (se existir): `pytest` na raiz.
- Conferir visualmente em `/` logado e deslogado, e comparar `/login` nas mesmas larguras (1280px, 768px, 375px).
- Checar acessibilidade: um único `h1` por página, `aria-live` nos feedbacks, `:focus-visible` nos novos painéis.