# Roteiro de apresentação e demonstração

## Objetivo

Apresentar em aproximadamente 10 minutos o problema, a proposta, o funcionamento do protótipo, os resultados técnicos, as limitações e os próximos passos.

## Estrutura sugerida

### 1. Problema identificado

- Resíduos em corpos d'água urbanos podem estar registrados de forma dispersa.
- Fotografias e coordenadas isoladas dificultam comparação ao longo do tempo.
- Sem histórico organizado, é difícil identificar recorrência e priorizar observações.

### 2. Justificativa

- Dados georreferenciados tornam observações comparáveis.
- Uma interface responsiva e acessível permite registrar, visualizar e exportar informações com feedback claro.
- O projeto apoia estudo e monitoramento; não substitui órgãos ambientais.

### 3. Solução proposta

Apresentar o fluxo:

> registrar → validar → localizar → visualizar → analisar → acompanhar → comparar → exportar

Destacar:

- mapa interativo;
- pontos monitorados e histórico;
- filtros e dashboard;
- autenticação e perfis;
- exportação CSV/GeoJSON;
- validações e testes automatizados;
- identidade visual ambiental, responsividade e acessibilidade.

### 4. Arquitetura

- Frontend com templates Jinja, HTML, JavaScript por página e duas camadas de CSS (`style.css` e `ui.css`).
- Backend Flask organizado em rotas, serviços e repositórios.
- SQLite para dados e pasta local para imagens.
- Leaflet/OpenStreetMap para mapas.
- Chart.js para gráficos.
- Pillow para validação de imagens e pytest para qualidade.

### 5. Demonstração do protótipo

Preparação:

1. Executar `.venv/bin/python app.py`.
2. Abrir `http://127.0.0.1:5000`.
3. Confirmar dados seed e disponibilidade da internet para mapas/CDNs.
4. Entrar com a conta de desenvolvimento.

Roteiro:

1. **Login:** demonstrar sessão e perfil.
2. **Registro:** mostrar formulário por etapas, feedback de localização, preview da fotografia e estado de envio.
3. **Mapa:** aplicar filtros combinados, mostrar total, clusterização, popup e exportações filtradas.
4. **Detalhe:** abrir ocorrência e mostrar status; administrador/moderador pode alterá-lo.
5. **Histórico:** abrir o ponto monitorado e comparar ocorrências relacionadas.
6. **Dashboard:** mostrar totais, distribuições, evolução e ranking.
7. **Exportação:** baixar CSV e GeoJSON, opcionalmente filtrados.
8. **UX/UI:** reduzir a janela para demonstrar adaptação móvel, navegação, estados vazios e foco visível.
9. **Qualidade:** citar Pillow, limite de 10 MB, cookies/headers protegidos, logs sem dados sensíveis e 20 testes.

Plano alternativo sem internet:

- Demonstrar páginas e API locais.
- Usar capturas previamente preparadas para tiles e gráficos dependentes de CDN.
- Explicar que falhas externas não impedem acesso aos dados no SQLite.

### 6. Resultados

Resultados técnicos atuais:

- Fases 1 a 6 concluídas; Fase 7 é a próxima.
- CRUD, monitoramento, gestão, análise e exportação operacionais.
- 20 testes automatizados aprovados em banco temporário.
- Upload falso rejeitado e limite de tamanho validado.
- Interface reformulada em todas as páginas, com responsividade, acessibilidade, preview e feedback de carregamento.

Resultados de campo:

- Ainda não existem resultados de coleta formal.
- Os registros atuais são dados de exemplo e testes funcionais.
- A coleta e validação ambiental pertencem à Fase 7.

### 7. Limitações

- Banco e imagens locais.
- Critérios visuais ainda não calibrados em campo.
- Credencial seed apenas para desenvolvimento.
- Sem recuperação de senha, CSRF dedicado ou auditoria completa.
- Dependência de internet para mapa, gráficos e integrações externas.
- Regras de recorrência e criticidade simplificadas.

### 8. Possibilidades futuras

- Teste de campo e refinamento metodológico.
- PostgreSQL/PostGIS e armazenamento de objetos.
- Auditoria, segurança de produção e otimização de imagens.
- Consolidar na interface os adaptadores de Overpass, Open-Meteo, Nominatim e sensores já existentes no backend.
- Configurar gateways e credenciais exclusivamente no servidor.
- Índice de criticidade validado.
- Visão computacional e alertas após formação de histórico confiável.

## Encerramento sugerido

> O Igarapé Limpo não pretende resolver sozinho a poluição dos igarapés. O objetivo é transformar observações ambientais em dados georreferenciados que possam ser visualizados, comparados e acompanhados ao longo do tempo.

## Checklist antes da apresentação

- Executar `.venv/bin/pytest -q`.
- Verificar login e logout.
- Confirmar mapa, dashboard e detalhes.
- Verificar desktop e viewport móvel.
- Confirmar preview da fotografia e estados de carregamento.
- Navegar por teclado e verificar foco visível.
- Confirmar carregamento das fontes, Leaflet e Chart.js.
- Preparar uma ocorrência de demonstração sem dados pessoais.
- Confirmar exportações CSV e GeoJSON.
- Não usar dados seed como evidência de resultado ambiental.
- Ter capturas de tela como contingência.
- Encerrar o servidor após a demonstração.
