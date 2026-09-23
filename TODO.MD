TODO — Igarapé Limpo

Lista de etapas para desenvolvimento do protótipo.

---

# Painel de fases (status atual de implementação)

> Este painel mostra **em que fase estamos** e o que será feito a seguir,
> para você acompanhar exatamente o que está sendo atualizado no projeto.
> Cada fase é implementada em blocos, e o check de cada item é marcado em `<FASE_N>` no corpo abaixo.

| # | Fase | Status | Escopo principal |
|---|------|--------|------------------|
| 1 | Fundamentos (MVP) | ✅ **Concluída** | Backend, Frontend, Mapa, banco, API CRUD |
| 2 | Monitoramento (V2) | ✅ **Concluída** | Ponto monitorado, histórico, filtros, dashboard |
| 3 | Gestão (V2.1) | ✅ **Concluída** | Autenticação, perfis, permissões e status |
| 4 | Dados (V2.2) | ✅ **Concluída** | Exportação CSV/GeoJSON e análises |
| 5 | Qualidade e Segurança | ✅ **Concluída** | Pillow, privacidade, cookies, headers, logs e 20 testes |
| 6 | Documentação e Apresentação | ✅ **Concluída** | README, API, arquitetura, demo |
| Pós-Fase 6 | Reformulação UX/UI | ✅ **Concluída** | Identidade visual, responsividade, acessibilidade e feedbacks |
| 7 | Pesquisa e Teste de campo | ⏳ **Próxima** | Fontes de dados, metodologia, coleta |
| Futuro | Visão computacional | 🔮 Futuro | Classificação automática por imagem |
| Futuro | Alertas | 🔮 Futuro | Detecção de tendências e notificações |

## Próxima fase: **FASE 7 — Pesquisa e Teste de campo**

Próximos passos nesta fase (na ordem):

1. Definir área inicial e fontes de dados.
2. Validar metodologia e critérios com participantes responsáveis.
3. Executar coleta de campo controlada.
4. Avaliar precisão, usabilidade e comportamento em dispositivos reais.
5. Registrar resultados e correções necessárias.

Os itens desta fase estão marcados com `[ ] <FASE7>` no corpo abaixo.

---

1. Definição do projeto

MVP definido (protótipo implementado):

- [x] Definir nome definitivo do projeto.
- [x] Definir objetivo geral.
- [x] Definir objetivos específicos.
- [x] Definir público-alvo.
- [ ] <FASE7> Definir área inicial de monitoramento.
- [x] Definir quais tipos de resíduos serão registrados.
- [x] Definir níveis de acúmulo.
- [x] Definir quais dados serão armazenados.
- [x] Definir quais funcionalidades pertencem ao MVP.
- [x] Registrar o escopo que ficará fora da primeira versão.

2. Pesquisa e validação

- [x] Fundamentar a problemática com fontes sobre a situação dos igarapés urbanos de Manaus (relatório técnico, seção 3).
- [ ] <FASE7> Pesquisar trabalhos existentes sobre monitoramento de resíduos em igarapés.
- [ ] <FASE7> Pesquisar sistemas semelhantes.
- [ ] <FASE7> Verificar quais dados ambientais já são disponibilizados publicamente.
- [ ] <FASE7> Identificar possíveis fontes de dados geográficos.
- [ ] <FASE7> Verificar quais informações podem ser coletadas pelos usuários.
- [ ] <FASE7> Identificar limitações legais e éticas relacionadas a fotografias e localização.
- [ ] <FASE7> Definir metodologia de coleta das ocorrências.

3. Modelagem do sistema

- [x] Definir fluxo principal da aplicação.
- [x] Criar diagrama de funcionamento.
- [x] Definir arquitetura frontend/backend.
- [x] Definir API.
- [x] Definir estrutura do banco de dados.
- [x] <FASE3> Definir modelo de usuário (previsto na evolução V2.1).
- [x] Definir modelo de ocorrência.
- [x] Definir modelo de localização.
- [x] Definir modelo de fotografia.
- [x] <FASE2> Definir relacionamento entre ocorrências e pontos monitorados (evolução V2).

4. Banco de dados

- [x] Criar banco SQL.
- [x] <FASE3> Criar tabela de usuários (evolução V2.1).
- [x] Criar tabela de ocorrências.
- [x] Definir tabela de tipos de resíduos.
- [x] Definir tabela de níveis de acúmulo.
- [x] Criar campos de latitude e longitude.
- [x] Criar campos de data e horário.
- [x] Criar relacionamento entre registros.
- [x] Criar dados de teste.
- [x] Testar inserção, alteração e consulta.
- [x] Criar consultas para estatísticas básicas.
- [x] <FASE2> Criar tabela de pontos monitorados (evolução V2).
- [x] <FASE2> Adicionar campos de status e ponto_id às ocorrências (evolução V2).

5. Backend

- [x] Criar projeto backend.
- [x] Configurar conexão com o banco.
- [x] Criar endpoint para cadastrar ocorrência.
- [x] Criar endpoint para consultar ocorrências.
- [x] Criar endpoint para consultar uma ocorrência específica.
- [x] Criar endpoint para atualizar ocorrência.
- [x] Criar endpoint para excluir ocorrência.
- [x] Implementar recebimento das coordenadas.
- [x] Implementar recebimento das informações da ocorrência.
- [x] Implementar upload de fotografia.
- [x] Validar os dados recebidos.
- [x] Implementar tratamento de erros.
- [x] Testar API.

6. Frontend

- [x] Criar estrutura inicial da aplicação.
- [x] Criar página inicial.
- [x] Criar tela de registro de ocorrência.
- [x] Criar formulário de ocorrência.
- [x] Implementar obtenção da localização.
- [x] Implementar seleção manual da localização.
- [x] Implementar envio de fotografia.
- [x] Implementar seleção do tipo de resíduo.
- [x] Implementar seleção do nível de acúmulo.
- [x] Conectar formulário à API.
- [x] Criar tela de consulta das ocorrências.

Frontend — evolução V2:

- [x] <FASE2> Adicionar filtros e pesquisa (tipo, nível, período, local).
- [x] <UX/UI> Adicionar preview de fotografia no formulário.
- [x] <UX/UI> Adicionar estado de carregamento no envio.
- [x] <FASE2> Criar página de ponto monitorado.
- [x] <FASE2> Criar página de dashboard com gráficos.
- [x] <FASE3> Criar página de login.

Frontend — reformulação UX/UI:

- [x] <UX/UI> Criar identidade visual ambiental e sistema de componentes.
- [x] <UX/UI> Reformular navegação, mapa, dashboard, formulários, login e detalhes.
- [x] <UX/UI> Adaptar layouts para desktop, tablet e celular.
- [x] <UX/UI> Adicionar estados vazios, falhas de rede e feedbacks contextuais.
- [x] <UX/UI> Melhorar acessibilidade com skip link, foco visível, ARIA e redução de movimento.
- [x] <UX/UI> Sincronizar exportações com os filtros do mapa.
- [x] <UX/UI> Sanitizar conteúdo dinâmico de popups e listas.

7. Mapa

- [x] Escolher biblioteca ou serviço de mapas.
- [x] Integrar mapa ao frontend.
- [x] Exibir posição das ocorrências.
- [x] Criar marcadores.
- [x] Diferenciar níveis de acúmulo visualmente.
- [x] Criar janela de informações do marcador.
- [x] Exibir fotografia da ocorrência.
- [x] Exibir data e horário.
- [x] Exibir tipo de resíduo.
- [x] <FASE2> Criar filtros básicos (evolução V2).
- [x] Testar mapa com dados reais de exemplo.

Mapa — evolução V2:

- [x] <FASE2> Adicionar filtros combináveis no mapa.
- [x] <FASE2> Adicionar pesquisa por local.
- [x] <FASE2> Exibir somente pontos críticos.
- [x] <FASE2> Centralizar no ponto selecionado.
- [x] <FASE2> Agrupar (clusterizar) marcadores com plugin do Leaflet.
- [x] <FASE2> Exibir histórico do ponto no popup/página.

8. Histórico e análise

- [x] <FASE2> Criar página de histórico.
- [x] <FASE2> Agrupar ocorrências por localização.
- [x] <FASE2> Identificar pontos recorrentes.
- [x] <FASE2> Criar contagem de ocorrências.
- [x] <FASE2> Criar estatísticas por tipo de resíduo.
- [x] <FASE2> Criar estatísticas por região.
- [x] <FASE2> Criar evolução temporal.
- [x] <FASE2> Criar dashboard básico.

9. Teste de campo

- [ ] <FASE7> Escolher primeiro trecho de monitoramento.
- [ ] <FASE7> Definir procedimento de coleta.
- [ ] <FASE7> Realizar primeira coleta.
- [ ] <FASE7> Registrar fotografias.
- [ ] <FASE7> Registrar coordenadas.
- [ ] <FASE7> Cadastrar ocorrências no sistema.
- [ ] <FASE7> Verificar precisão das localizações.
- [ ] <FASE7> Verificar qualidade das fotografias.
- [ ] <FASE7> Identificar problemas de usabilidade.
- [ ] <FASE7> Corrigir problemas encontrados.
- [ ] <FASE7> Repetir coleta.
- [ ] <FASE7> Comparar os dados coletados.

10. Protótipo de visão computacional

Etapa posterior ao funcionamento do MVP.

- [ ] <FUTURO> Montar conjunto inicial de imagens.
- [ ] <FUTURO> Definir classes de resíduos.
- [ ] <FUTURO> Organizar e etiquetar as imagens.
- [ ] <FUTURO> Pesquisar modelos adequados.
- [ ] <FUTURO> Escolher abordagem de classificação.
- [ ] <FUTURO> Treinar ou adaptar modelo.
- [ ] <FUTURO> Testar modelo.
- [ ] <FUTURO> Medir taxa de acerto.
- [ ] <FUTURO> Comparar classificação automática e manual.
- [ ] <FUTURO> Integrar modelo ao backend.
- [ ] <FUTURO> Exibir resultado da classificação no sistema.

11. Alertas

Etapa posterior.

- [ ] <FUTURO> Definir o que caracteriza aumento significativo de resíduos.
- [ ] <FUTURO> Criar regra para identificar crescimento de ocorrências.
- [ ] <FUTURO> Criar sistema de alerta.
- [ ] <FUTURO> Exibir pontos em situação de atenção.
- [ ] <FUTURO> Testar alertas com dados históricos.

12. Qualidade e segurança

- [x] <FASE5> Validar dados recebidos pela API.
- [x] <FASE5> Validar arquivos enviados.
- [x] <FASE5> Limitar tamanho das fotografias.
- [x] <FASE5> Implementar tratamento adequado de erros.
- [x] <FASE5> Evitar exposição desnecessária de dados pessoais.
- [ ] <FASE7> Testar diferentes dispositivos.
- [ ] <FASE7> Testar conexão lenta.
- [ ] <FASE7> Testar comportamento sem localização disponível.
- [x] <FASE7> Testar comportamento sem fotografia.
- [x] <FASE7> Revisar permissões de localização.

13. Documentação

- [x] <FASE6> Atualizar README.
- [x] <FASE6> Documentar arquitetura.
- [x] <FASE6> Documentar banco de dados.
- [x] <FASE6> Documentar API.
- [x] <FASE6> Documentar metodologia de coleta.
- [x] <FASE6> Documentar critérios de classificação.
- [x] <FASE6> Registrar decisões técnicas.
- [x] <FASE6> Registrar limitações do protótipo.

## Entregas técnicas posteriores

- [x] Implementar comparação entre períodos no dashboard.
- [x] Implementar alerta agregado para aumento de ocorrências.
- [x] Cobrir ausência de fotografia e falha de geolocalização com feedback na interface.
- [ ] Validar responsividade em dispositivos físicos.
- [ ] Validar operação sob conexão lenta ou indisponível.
- [ ] Criar classificação automática com conjunto de imagens rotuladas.
- [x] <FASE6> Registrar resultados dos testes.
- [x] <FASE6> Documentar possíveis trabalhos futuros.

14. Apresentação final

- [x] <FASE6> Preparar demonstração do protótipo.
- [x] <FASE6> Preparar problema identificado.
- [x] <FASE6> Apresentar justificativa.
- [x] <FASE6> Apresentar solução.
- [x] <FASE6> Demonstrar registro de ocorrência.
- [x] <FASE6> Demonstrar mapa.
- [x] <FASE6> Demonstrar histórico.
- [x] <FASE6> Apresentar resultados técnicos e informar que a coleta de campo ainda não ocorreu.
- [x] <FASE6> Apresentar limitações.
- [x] <FASE6> Apresentar possibilidades futuras.

Sequência histórica/original de desenvolvimento

Pesquisa
   ↓
Definição do MVP
   ↓
Modelagem
   ↓
Banco SQL
   ↓
Backend
   ↓
Frontend
   ↓
Mapa
   ↓
Integração
   ↓
Teste de campo
   ↓
Correções
   ↓
Dashboard
   ↓
Visão computacional
   ↓
Alertas

Regra de escopo

O protótipo não deve começar pelas funcionalidades avançadas.

A prioridade é:

«Registrar → armazenar → localizar → visualizar → analisar.»

Somente depois:

«Classificar automaticamente → detectar tendências → gerar alertas.»

A inteligência artificial é uma possível evolução do projeto, não um requisito para que o protótipo seja considerado funcional.

Sequência atual:

Pesquisa e validação
   ↓
Coleta de campo controlada
   ↓
Avaliação em dispositivos e conexões reais
   ↓
Correções de usabilidade e metodologia
   ↓
Calibração dos critérios ambientais

---

# Histórico de progresso

> Registro do que foi implementado em cada sessão, para acompanhamento
> e para que não haja perda de contexto entre sessões.

## Sessão 2026-09-23 (Relatório técnico e fundamentação)

Concluído:

- Adicionados os integrantes ao relatório técnico: Daniel Fernandes de Oliveira da Silva, Adriano Alves Barros, Carlos Johnatan Silva Souza Rodrigues e Julio Thiago Colares de Lima.
- Criada a seção 3 (Fundamentação) do `RELATORIO.md`, com referências [1] a [7] sobre a situação dos igarapés urbanos de Manaus.
- Armazenadas as fotografias do relatório no cofre do Obsidian (`docs/obsidian/07 - Relatório`), mantendo as Figuras 2 e 3.
- Renomeada toda a documentação e o README da raiz para o nome do projeto (Igarapé Limpo), padronizando com o relatório.
- Removidas as imagens jpeg da raiz do projeto (igarape1.jpeg e igarape2.jpeg).

Pendente: pesquisa de campo, coleta de fotografias em igarapés, fundamentação com artigos científicos e testes em campo.

## Sessão 2026-08-30 (Reformulação UX/UI)

Concluído:

- Criado `static/css/ui.css` com nova identidade visual, componentes e breakpoints responsivos.
- Reformulados cabeçalho, mapa, filtros, dashboard, formulário, login, ocorrência, ponto e página 404.
- Adicionados preview de fotografia, estados de carregamento, estados vazios e mensagens de falha.
- Adicionadas melhorias de acessibilidade, incluindo skip link, foco visível, ARIA e reduced motion.
- Atualizados scripts do mapa e dashboard para feedback de rede, exportações filtradas e renderização segura.
- Mantidos 20 testes automatizados aprovados após a reformulação.

Próximo passo registrado nesta sessão: **Fase 7 — Pesquisa e Teste de campo**.

## Sessão 2026-08-30 (Fase 6 — Documentação e Apresentação)

Concluído:

- Criado `DOCUMENTACAO.md` com banco, API, metodologia, critérios, decisões, testes, limitações e trabalhos futuros.
- Criado `APRESENTACAO.md` com estrutura, roteiro de demonstração, contingência e checklist.
- Atualizado README com o estado implementado, testes e referências documentais.
- Diferenciados resultados técnicos, dados seed e resultados de campo ainda não coletados.

Próximo passo registrado naquela sessão: **Fase 7 — Pesquisa e Teste de campo**.

## Sessão 2026-08-30 (Fase 5 — Qualidade e Segurança)

Concluído:

- Corrigido o tratamento de credenciais inválidas, identificado pelos testes automatizados.
- Removidos `senha_hash` e `usuario_id` das respostas públicas.
- Adicionadas validações de tamanho para textos, credenciais e pesquisas.
- Uploads agora validam extensão e conteúdo real da imagem com Pillow, mantendo o limite de 10 MB.
- Adicionados cookies de sessão protegidos, cabeçalhos HTTP de segurança e erro 500 genérico na API.
- Adicionados logs de login, logout, criação de usuário e operações sobre ocorrências sem dados sensíveis.
- Criada suíte automatizada isolada do banco principal, com 20 testes cobrindo autenticação, filtros, exportações, uploads e páginas.

Próximo passo registrado naquela sessão: **Fase 6 — Documentação e Apresentação**.

## Sessão 2026-08-30 (Fase 4 — Dados V2.2)

Concluído:

- Adicionados botões de exportação em CSV e GeoJSON no dashboard, página inicial e página de ponto monitorado.
- Exportações passaram a aceitar filtros por query string (tipo, nível, período, ponto_id, busca).
- Atualizado painel de fases: Fase 4 marcada como concluída.

Próximo passo registrado naquela sessão: **Fase 5 — Qualidade e Segurança**.

## Sessão 2026-08-30 (fundamentos / MVP)

Concluído:

- Corrigida a refatoração quebrada para o pacote `app/`:
  - criado `app/__init__.py` com `create_app()` (factory);
  - criado `app/routes/pages.py` (páginas `/`, `/nova`, `/ocorrencia/<id>`, 404);
  - resolvido o conflito entre o módulo `app.py` e o pacote `app/`;
  - apontados `template_folder` e `static_folder` para a raiz do projeto;
  - atualizados os `url_for('pages.*')` nos templates.
- Completado o CRUD de ocorrências no backend:
  - `PUT /api/ocorrencias/<id>` (atualizar, com troca de fotografia);
  - `DELETE /api/ocorrencias/<id>` (excluir, removendo a foto do disco);
  - métodos de `atualizar`/`excluir` no repositório e serviço.
- Marcada toda a seção **5. Backend** como concluída no corpo do TODO.
- Atualizado o README (status do MVP, API CRUD, integrações e arquitetura).
- Validação de ponta a ponta: páginas, CRUD, upload de foto, exportação CSV,
  validação de dados e erros (400/404/413).

Observação: o projeto já conta com integrações auxiliares implementadas
(hidrografia via Overpass, meteorologia via Open-Meteo, geocodificação via
Nominatim e gateway de sensores) e endpoint de exportação em CSV, que estão
implementados mas ainda não constavam como itens do TODO original.

Próximo passo registrado naquela sessão: **FASE 2 — Monitoramento**.
