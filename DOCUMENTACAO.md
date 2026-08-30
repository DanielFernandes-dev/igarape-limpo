# Documentação técnica e metodológica

## 1. Escopo

O Igarapé Vivo registra ocorrências georreferenciadas de resíduos, associa registros a pontos monitorados, apresenta histórico e indicadores e exporta dados em CSV e GeoJSON.

Esta documentação descreve o estado implementado até a Fase 5. Visão computacional, alertas e resultados de coleta de campo não fazem parte da versão atual.

## 2. Banco de dados

O protótipo usa SQLite no arquivo `igarape_vivo.db`. O schema inicial está em `schema.sql`; `database.py` aplica evoluções idempotentes em bancos existentes.

### 2.1. `usuarios`

| Campo | Tipo | Regra |
|---|---|---|
| `id` | INTEGER | Chave primária |
| `nome` | TEXT | Obrigatório, até 120 caracteres |
| `email` | TEXT | Obrigatório e único, até 254 caracteres |
| `senha_hash` | TEXT | Hash gerado pelo Werkzeug; nunca retornado pela API |
| `perfil` | TEXT | `usuario`, `moderador` ou `administrador` |
| `ativo` | INTEGER | `1` ativo, `0` inativo |
| `data_criacao` | TEXT | Data UTC gerada pelo SQLite |

### 2.2. `pontos_monitorados`

| Campo | Tipo | Regra |
|---|---|---|
| `id` | INTEGER | Chave primária |
| `nome` | TEXT | Obrigatório, até 120 caracteres |
| `latitude` | REAL | Entre -90 e 90 |
| `longitude` | REAL | Entre -180 e 180 |
| `descricao` | TEXT | Opcional, até 1000 caracteres |
| `status` | TEXT | `Ativo` ou `Inativo` |
| `data_criacao` | TEXT | Data UTC gerada pelo SQLite |

### 2.3. `ocorrencias`

| Campo | Tipo | Regra |
|---|---|---|
| `id` | INTEGER | Chave primária |
| `ponto_id` | INTEGER | Referência opcional a `pontos_monitorados` |
| `usuario_id` | INTEGER | Referência opcional a `usuarios`; não exposta publicamente |
| `latitude` | REAL | Entre -90 e 90 |
| `longitude` | REAL | Entre -180 e 180 |
| `data_hora` | TEXT | Data UTC gerada pelo SQLite |
| `fotografia` | TEXT | Nome interno do arquivo, opcional |
| `tipo_residuo` | TEXT | Domínio controlado |
| `nivel_acumulo` | TEXT | `Baixo`, `Medio` ou `Alto` |
| `status` | TEXT | `Nova`, `Em analise`, `Em atendimento`, `Resolvida` ou `Descartada` |
| `observacoes` | TEXT | Opcional, até 2000 caracteres |
| `local_nome` | TEXT | Opcional, até 160 caracteres |
| `data_atualizacao` | TEXT | Atualizada em alterações |

Índices atuais: coordenadas de ocorrências e coordenadas de pontos. Consultas futuras em maior escala devem adicionar índices por data, tipo, nível, ponto e status.

## 3. API HTTP

Prefixo: `/api`. Respostas de sucesso usam JSON, exceto exportações CSV. Erros usam `{"erro": "mensagem"}`.

### 3.1. Autenticação

| Método | Rota | Acesso | Descrição |
|---|---|---|---|
| POST | `/auth/login` | Público | Inicia sessão com JSON `email` e `senha` |
| POST | `/auth/logout` | Público | Encerra a sessão atual |
| GET | `/auth/me` | Autenticado | Retorna usuário sem hash de senha |
| GET | `/auth/usuarios` | Moderador/Admin | Lista usuários |
| POST | `/auth/usuarios` | Admin | Cria usuário |

Exemplo de login:

```http
POST /api/auth/login
Content-Type: application/json

{"email":"admin@igarape.local","senha":"admin123"}
```

O usuário seed é exclusivo para desenvolvimento. A senha deve ser substituída antes de qualquer implantação acessível externamente.

### 3.2. Ocorrências

| Método | Rota | Acesso | Descrição |
|---|---|---|---|
| GET | `/ocorrencias` | Público | Lista ocorrências com filtros |
| GET | `/ocorrencias/<id>` | Público | Obtém uma ocorrência |
| POST | `/ocorrencias` | Autenticado | Cria ocorrência via `multipart/form-data` |
| PUT/PATCH | `/ocorrencias/<id>` | Autenticado | Atualiza ocorrência; PATCH aceita JSON parcial |
| DELETE | `/ocorrencias/<id>` | Moderador/Admin | Exclui ocorrência e fotografia |

Filtros combináveis:

- `tipo_residuo`
- `nivel_acumulo`
- `ponto_id`
- `data_inicio` e `data_fim` em `AAAA-MM-DD`
- `busca` em local e observações

### 3.3. Pontos monitorados

| Método | Rota | Acesso | Descrição |
|---|---|---|---|
| GET | `/pontos` | Público | Lista pontos e contagens |
| GET | `/pontos/<id>` | Público | Retorna resumo do ponto |
| POST | `/pontos` | Moderador/Admin | Cria ponto |
| PUT/PATCH | `/pontos/<id>` | Moderador/Admin | Atualiza ponto |
| GET | `/pontos/<id>/historico` | Público | Lista histórico do ponto |

### 3.4. Dashboard e exportação

| Método | Rota | Descrição |
|---|---|---|
| GET | `/dashboard/resumo` | Totais e distribuições |
| GET | `/dashboard/series?dias=30` | Série temporal de 1 a 365 dias |
| GET | `/dashboard/ranking?limite=10` | Ranking de pontos |
| GET | `/export/ocorrencias.csv` | Exporta ocorrências; aceita os filtros da listagem |
| GET | `/export/ocorrencias.geojson` | Exporta `FeatureCollection`; aceita filtros |

### 3.5. Integrações

| Método | Rota | Serviço |
|---|---|---|
| GET | `/integracao/hidrografia` | Overpass/OpenStreetMap |
| GET | `/integracao/meteo?lat=&lon=` | Open-Meteo |
| GET | `/integracao/geocode?lat=&lon=` | Nominatim |
| POST | `/integracao/sensores` | Gateway JSON informado no corpo |
| GET | `/integracao/status` | Estado configurado das integrações |
| POST | `/export/sensores.csv` | Exporta dados do gateway |

Serviços externos podem retornar `502` sem impedir o funcionamento do mapa e do banco local.

## 4. Metodologia de coleta proposta

1. Definir previamente trecho, ponto de referência e horário da observação.
2. Obter localização pelo dispositivo ou marcar manualmente no mapa.
3. Confirmar visualmente se a coordenada corresponde ao local observado.
4. Registrar uma fotografia contextual, evitando rostos, placas e informações pessoais.
5. Classificar o tipo predominante de resíduo e o nível de acúmulo.
6. Associar a um ponto monitorado existente quando a observação for recorrente.
7. Descrever apenas informações ambientais necessárias.
8. Revisar os dados antes do envio.
9. Repetir a observação no mesmo ponto em datas posteriores.
10. Registrar limitações da coleta, como chuva, acesso, GPS impreciso ou ausência de fotografia.

O protótipo ainda não executou coleta de campo formal. A metodologia deve ser validada na Fase 7 antes de ser tratada como protocolo definitivo.

## 5. Critérios de classificação

### Tipo de resíduo

- `Plastico`: garrafas, sacolas e embalagens plásticas.
- `Metal`: latas, peças e sucata metálica.
- `Vidro`: garrafas, frascos e fragmentos de vidro.
- `Organico`: restos vegetais ou alimentares de origem orgânica.
- `Papel`: papel, papelão e materiais semelhantes.
- `Misto`: mais de uma categoria sem predominância clara.
- `Outro`: material fora das categorias anteriores, descrito em observações.

### Nível de acúmulo

- `Baixo`: poucos itens isolados, sem bloqueio visível do fluxo.
- `Medio`: concentração perceptível, ainda localizada.
- `Alto`: grande concentração, espalhamento relevante ou possível obstrução.

Esses níveis são estimativas visuais do protótipo, não uma métrica ambiental oficial. A calibração depende de validação em campo.

### Recorrência e criticidade

Atualmente, um ponto é considerado recorrente quando possui pelo menos três ocorrências no histórico total. No filtro do mapa, “pontos críticos” significa ocorrências com nível `Alto`. A janela de 90 dias existe como referência de evolução, mas ainda não limita o cálculo de recorrência.

## 6. Decisões técnicas

- Flask e JavaScript puro mantêm o protótipo simples e fácil de executar.
- SQLite atende desenvolvimento e validação com baixa concorrência.
- Camadas de rotas, serviços e repositórios separam HTTP, regras e persistência.
- Leaflet/OpenStreetMap evita dependência de chave comercial.
- Fotografias ficam em `static/uploads` com nome UUID.
- Pillow verifica o conteúdo real das imagens; o limite total da requisição é 10 MB.
- Sessões usam cookies `HttpOnly` e `SameSite=Lax`; `Secure` é ativado por `IGARAPE_HTTPS=1`.
- Respostas públicas removem `senha_hash` e `usuario_id`.
- CSV e GeoJSON facilitam análise externa e interoperabilidade geográfica.

## 7. Resultados dos testes

Em 30/08/2026, a suíte automatizada executou 20 testes com sucesso:

- páginas principais;
- autenticação válida e inválida;
- proteção de rotas;
- filtros por tipo, nível e ponto;
- resumo do dashboard;
- exportações CSV e GeoJSON;
- ausência de identificador de usuário na API pública;
- ocorrência sem fotografia;
- aceitação de PNG válido;
- rejeição de arquivo falso;
- limite de upload com resposta `413`;
- cabeçalhos HTTP de segurança.

Comando:

```bash
.venv/bin/pytest -q
```

Os testes usam banco e pasta de uploads temporários, sem modificar os dados locais.

## 8. Limitações

- Não há resultados ambientais reais nem validação da metodologia em campo.
- SQLite e armazenamento local não são indicados para alta concorrência.
- O usuário seed possui credencial conhecida para desenvolvimento.
- Não há recuperação de senha, segundo fator ou proteção CSRF dedicada.
- Usuários autenticados podem atualizar ocorrências que não criaram.
- O gateway de sensores aceita URL informada pelo cliente e precisa de restrição antes de produção.
- Dependências de CDN e serviços externos exigem conexão para recursos completos.
- Recorrência e criticidade ainda usam regras simplificadas.
- A fotografia é validada, mas não é redimensionada nem tem metadados removidos.

## 9. Trabalhos futuros

- Executar coleta de campo e calibrar critérios.
- Adicionar propriedade e auditoria completa das alterações.
- Restringir destinos do gateway para evitar requisições indevidas.
- Implementar proteção CSRF, recuperação de senha e política de credenciais.
- Remover metadados e gerar versões otimizadas das imagens.
- Migrar para PostgreSQL/PostGIS quando a escala justificar.
- Criar índice de criticidade validado por frequência, intensidade e recência.
- Integrar fontes oficiais e telemetria configurada no servidor.
- Avaliar visão computacional somente após formar conjunto de dados confiável.
- Criar alertas após validar tendências com histórico real.
