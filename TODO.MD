TODO — Igarapé Vivo

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
| 4 | Dados (V2.2) | ⏳ Próxima | Exportação CSV/GeoJSON e análises |
| 5 | Qualidade e Segurança | ⏳ Depois | Validações, testes, limites de arquivo |
| 6 | Documentação e Apresentação | ⏳ Depois | README, API, arquitetura, demo |
| 7 | Pesquisa e Teste de campo | ⏳ Depende de decisões | Fontes de dados, metodologia, coleta |
| Futuro | Visão computacional | 🔮 Futuro | Classificação automática por imagem |
| Futuro | Alertas | 🔮 Futuro | Detecção de tendências e notificações |

## Fase atual: **FASE 2 — Monitoramento (V2)**

Próximos passos nesta fase (na ordem):

1. Criar tabela de **pontos monitorados** e associar ocorrências (`ponto_id`).
2. Criar repositório, serviço e rotas de **pontos monitorados**.
3. Adicionar **filtros** (tipo, nível, período, local) na listagem/mapa.
4. Criar **página do ponto monitorado** com histórico.
5. Criar **página de dashboard** com gráficos e estatísticas.

Os itens desta fase estão marcados com `[ ] <FASE2>` no corpo abaixo e podem ser
acompanhados por busca (`Ctrl+F`: **FASE2**). Quando uma fase termina, o check é
marcado e o bloco `<FASE_N>` passa a `[x]`.

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
- [ ] <FASE7> Adicionar preview de fotografia no formulário.
- [ ] <FASE7> Adicionar indicador de progresso/carregamento no envio.
- [x] <FASE2> Criar página de ponto monitorado.
- [x] <FASE2> Criar página de dashboard com gráficos.
- [x] <FASE3> Criar página de login.

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
- [ ] <FASE5> Evitar exposição desnecessária de dados pessoais.
- [ ] <FASE7> Testar diferentes dispositivos.
- [ ] <FASE7> Testar conexão lenta.
- [ ] <FASE7> Testar comportamento sem localização disponível.
- [ ] <FASE7> Testar comportamento sem fotografia.
- [ ] <FASE7> Revisar permissões de localização.

13. Documentação

- [x] <FASE6> Atualizar README.
- [x] <FASE6> Documentar arquitetura.
- [ ] <FASE6> Documentar banco de dados.
- [ ] <FASE6> Documentar API.
- [ ] <FASE6> Documentar metodologia de coleta.
- [ ] <FASE6> Documentar critérios de classificação.
- [ ] <FASE6> Registrar decisões técnicas.
- [ ] <FASE6> Registrar limitações do protótipo.
- [ ] <FASE6> Registrar resultados dos testes.
- [ ] <FASE6> Documentar possíveis trabalhos futuros.

14. Apresentação final

- [ ] <FASE6> Preparar demonstração do protótipo.
- [ ] <FASE6> Preparar problema identificado.
- [ ] <FASE6> Apresentar justificativa.
- [ ] <FASE6> Apresentar solução.
- [ ] <FASE6> Demonstrar registro de ocorrência.
- [ ] <FASE6> Demonstrar mapa.
- [ ] <FASE6> Demonstrar histórico.
- [ ] <FASE6> Apresentar resultados da coleta.
- [ ] <FASE6> Apresentar limitações.
- [ ] <FASE6> Apresentar possibilidades futuras.

Ordem recomendada de desenvolvimento

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

---

# Histórico de progresso

> Registro do que foi implementado em cada sessão, para acompanhamento
> e para que não haja perda de contexto entre sessões.

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

Próximo passo: **FASE 2 — Monitoramento (V2)** (pontos monitorados, histórico,
filtros e dashboard).
