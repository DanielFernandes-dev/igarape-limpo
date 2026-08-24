TODO — Igarapé Vivo

Lista de etapas para desenvolvimento do protótipo.

1. Definição do projeto

- [ ] Definir nome definitivo do projeto.
- [ ] Definir objetivo geral.
- [ ] Definir objetivos específicos.
- [ ] Definir público-alvo.
- [ ] Definir área inicial de monitoramento.
- [ ] Definir quais tipos de resíduos serão registrados.
- [ ] Definir níveis de acúmulo.
- [ ] Definir quais dados serão armazenados.
- [ ] Definir quais funcionalidades pertencem ao MVP.
- [ ] Registrar o escopo que ficará fora da primeira versão.

2. Pesquisa e validação

- [ ] Pesquisar trabalhos existentes sobre monitoramento de resíduos em igarapés.
- [ ] Pesquisar sistemas semelhantes.
- [ ] Verificar quais dados ambientais já são disponibilizados publicamente.
- [ ] Identificar possíveis fontes de dados geográficos.
- [ ] Verificar quais informações podem ser coletadas pelos usuários.
- [ ] Identificar limitações legais e éticas relacionadas a fotografias e localização.
- [ ] Definir metodologia de coleta das ocorrências.

3. Modelagem do sistema

- [ ] Definir fluxo principal da aplicação.
- [ ] Criar diagrama de funcionamento.
- [ ] Definir arquitetura frontend/backend.
- [ ] Definir API.
- [ ] Definir estrutura do banco de dados.
- [ ] Definir modelo de usuário, caso login seja necessário.
- [ ] Definir modelo de ocorrência.
- [ ] Definir modelo de localização.
- [ ] Definir modelo de fotografia.
- [ ] Definir relacionamento entre ocorrências e pontos monitorados.

4. Banco de dados

- [ ] Criar banco SQL.
- [ ] Criar tabela de usuários, se necessária.
- [ ] Criar tabela de ocorrências.
- [ ] Criar tabela de tipos de resíduos.
- [ ] Criar tabela de níveis de acúmulo.
- [ ] Criar campos de latitude e longitude.
- [ ] Criar campos de data e horário.
- [ ] Criar relacionamento entre registros.
- [ ] Criar dados de teste.
- [ ] Testar inserção, alteração e consulta.
- [ ] Criar consultas para estatísticas básicas.

5. Backend

- [ ] Criar projeto backend.
- [ ] Configurar conexão com o banco.
- [ ] Criar endpoint para cadastrar ocorrência.
- [ ] Criar endpoint para consultar ocorrências.
- [ ] Criar endpoint para consultar uma ocorrência específica.
- [ ] Criar endpoint para atualizar ocorrência.
- [ ] Criar endpoint para excluir ocorrência, caso necessário.
- [ ] Implementar recebimento das coordenadas.
- [ ] Implementar recebimento das informações da ocorrência.
- [ ] Implementar upload de fotografia.
- [ ] Validar os dados recebidos.
- [ ] Implementar tratamento de erros.
- [ ] Testar API.

6. Frontend

- [ ] Criar estrutura inicial da aplicação.
- [ ] Criar página inicial.
- [ ] Criar tela de registro de ocorrência.
- [ ] Criar formulário de ocorrência.
- [ ] Implementar obtenção da localização.
- [ ] Implementar seleção manual da localização.
- [ ] Implementar envio de fotografia.
- [ ] Implementar seleção do tipo de resíduo.
- [ ] Implementar seleção do nível de acúmulo.
- [ ] Conectar formulário à API.
- [ ] Criar tela de consulta das ocorrências.

7. Mapa

- [ ] Escolher biblioteca ou serviço de mapas.
- [ ] Integrar mapa ao frontend.
- [ ] Exibir posição das ocorrências.
- [ ] Criar marcadores.
- [ ] Diferenciar níveis de acúmulo visualmente.
- [ ] Criar janela de informações do marcador.
- [ ] Exibir fotografia da ocorrência.
- [ ] Exibir data e horário.
- [ ] Exibir tipo de resíduo.
- [ ] Criar filtros básicos.
- [ ] Testar mapa com dados reais de exemplo.

8. Histórico e análise

- [ ] Criar página de histórico.
- [ ] Agrupar ocorrências por localização.
- [ ] Identificar pontos recorrentes.
- [ ] Criar contagem de ocorrências.
- [ ] Criar estatísticas por tipo de resíduo.
- [ ] Criar estatísticas por região.
- [ ] Criar evolução temporal.
- [ ] Criar dashboard básico.

9. Teste de campo

- [ ] Escolher primeiro trecho de monitoramento.
- [ ] Definir procedimento de coleta.
- [ ] Realizar primeira coleta.
- [ ] Registrar fotografias.
- [ ] Registrar coordenadas.
- [ ] Cadastrar ocorrências no sistema.
- [ ] Verificar precisão das localizações.
- [ ] Verificar qualidade das fotografias.
- [ ] Identificar problemas de usabilidade.
- [ ] Corrigir problemas encontrados.
- [ ] Repetir coleta.
- [ ] Comparar os dados coletados.

10. Protótipo de visão computacional

Etapa posterior ao funcionamento do MVP.

- [ ] Montar conjunto inicial de imagens.
- [ ] Definir classes de resíduos.
- [ ] Organizar e etiquetar as imagens.
- [ ] Pesquisar modelos adequados.
- [ ] Escolher abordagem de classificação.
- [ ] Treinar ou adaptar modelo.
- [ ] Testar modelo.
- [ ] Medir taxa de acerto.
- [ ] Comparar classificação automática e manual.
- [ ] Integrar modelo ao backend.
- [ ] Exibir resultado da classificação no sistema.

11. Alertas

Etapa posterior.

- [ ] Definir o que caracteriza aumento significativo de resíduos.
- [ ] Criar regra para identificar crescimento de ocorrências.
- [ ] Criar sistema de alerta.
- [ ] Exibir pontos em situação de atenção.
- [ ] Testar alertas com dados históricos.

12. Qualidade e segurança

- [ ] Validar dados recebidos pela API.
- [ ] Validar arquivos enviados.
- [ ] Limitar tamanho das fotografias.
- [ ] Implementar tratamento adequado de erros.
- [ ] Evitar exposição desnecessária de dados pessoais.
- [ ] Testar diferentes dispositivos.
- [ ] Testar conexão lenta.
- [ ] Testar comportamento sem localização disponível.
- [ ] Testar comportamento sem fotografia.
- [ ] Revisar permissões de localização.

13. Documentação

- [ ] Atualizar README.
- [ ] Documentar arquitetura.
- [ ] Documentar banco de dados.
- [ ] Documentar API.
- [ ] Documentar metodologia de coleta.
- [ ] Documentar critérios de classificação.
- [ ] Registrar decisões técnicas.
- [ ] Registrar limitações do protótipo.
- [ ] Registrar resultados dos testes.
- [ ] Documentar possíveis trabalhos futuros.

14. Apresentação final

- [ ] Preparar demonstração do protótipo.
- [ ] Preparar problema identificado.
- [ ] Apresentar justificativa.
- [ ] Apresentar solução.
- [ ] Demonstrar registro de ocorrência.
- [ ] Demonstrar mapa.
- [ ] Demonstrar histórico.
- [ ] Apresentar resultados da coleta.
- [ ] Apresentar limitações.
- [ ] Apresentar possibilidades futuras.

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
