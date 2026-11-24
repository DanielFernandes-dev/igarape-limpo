PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS usuarios (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE,
    senha_hash TEXT NOT NULL,
    perfil TEXT NOT NULL DEFAULT 'usuario',
    ativo INTEGER NOT NULL DEFAULT 1,
    data_criacao TEXT NOT NULL DEFAULT (datetime('now'))
);

CREATE TABLE IF NOT EXISTS pontos_monitorados (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    latitude REAL NOT NULL,
    longitude REAL NOT NULL,
    descricao TEXT,
    status TEXT NOT NULL DEFAULT 'Ativo',
    data_criacao TEXT NOT NULL DEFAULT (datetime('now')),
    nivel_acessibilidade TEXT,
    observacoes_acesso TEXT,
    data_avaliacao_acesso TEXT,
    responsavel_avaliacao_id INTEGER REFERENCES usuarios (id)
);

CREATE INDEX IF NOT EXISTS idx_pontos_coord
ON pontos_monitorados (latitude, longitude);

CREATE TABLE IF NOT EXISTS ocorrencias (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    ponto_id INTEGER REFERENCES pontos_monitorados (id),
    usuario_id INTEGER REFERENCES usuarios (id),
    latitude REAL NOT NULL,
    longitude REAL NOT NULL,
    data_hora TEXT NOT NULL DEFAULT (datetime('now')),
    fotografia TEXT,
    tipo_residuo TEXT NOT NULL,
    nivel_acumulo TEXT NOT NULL,
    status TEXT NOT NULL DEFAULT 'Nova',
    observacoes TEXT,
    local_nome TEXT,
    data_atualizacao TEXT,
    protocolo TEXT
);

CREATE UNIQUE INDEX IF NOT EXISTS idx_ocorrencias_protocolo_unico
ON ocorrencias (protocolo) WHERE protocolo IS NOT NULL;

CREATE INDEX IF NOT EXISTS idx_ocorrencias_ponto_data
ON ocorrencias (ponto_id, data_hora DESC);

CREATE TABLE IF NOT EXISTS limpezas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    ponto_id INTEGER NOT NULL REFERENCES pontos_monitorados (id) ON DELETE CASCADE,
    data_hora TEXT NOT NULL,
    equipe TEXT,
    quantidade REAL,
    unidade TEXT,
    fotografia TEXT,
    observacoes TEXT,
    usuario_id INTEGER REFERENCES usuarios (id),
    data_cadastro TEXT NOT NULL DEFAULT (datetime('now'))
);

CREATE INDEX IF NOT EXISTS idx_limpezas_ponto_data
ON limpezas (ponto_id, data_hora DESC);

CREATE INDEX IF NOT EXISTS idx_ocorrencias_coord
ON ocorrencias (latitude, longitude);

INSERT INTO pontos_monitorados (nome, latitude, longitude, descricao, status)
VALUES
    ('Igarapé do Mindu — Trecho 1', -3.059860, -60.040980, 'Margem próxima à passarela.', 'Ativo'),
    ('Igarapé do Mindu — Trecho 2', -3.057500, -60.047000, 'Ponte central, ponto de descarte frequente.', 'Ativo'),
    ('Igarapé do Educandos — Foz', -3.140000, -60.008000, 'Desembocadura do igarapé.', 'Ativo'),
    ('Igarapé do Quarenta — Trecho demonstrativo', -3.1307664, -59.9964426, 'Coordenada de referência do OpenStreetMap; validar em campo.', 'Ativo'),
    ('Igarapé Tarumã-Açu — Trecho demonstrativo', -2.9858251, -60.1261855, 'Coordenada de referência do OpenStreetMap; validar em campo.', 'Ativo');

INSERT INTO ocorrencias
    (ponto_id, latitude, longitude, data_hora, fotografia, tipo_residuo, nivel_acumulo, status, observacoes, local_nome)
VALUES
    (1, -3.059860, -60.040980, '2026-08-24 09:15:00', NULL, 'Plastico', 'Alto', 'Nova', 'Acúmulo grande próximo às margens, muitos sacos plásticos.', 'Igarapé do Mindu'),
    (4, -3.1307664, -59.9964426, '2026-08-25 14:30:00', NULL, 'Misto', 'Medio', 'Em analise', 'Garrafas pet e embalagens espalhadas.', 'Igarapé do Quarenta'),
    (5, -2.9858251, -60.1261855, '2026-08-26 10:05:00', NULL, 'Metal', 'Baixo', 'Resolvida', 'Poucas latas e ferros velhos.', 'Igarapé Tarumã-Açu'),
    (2, -3.063900, -60.042300, '2026-08-27 11:45:00', NULL, 'Organico', 'Alto', 'Em atendimento', 'Resíduos orgânicos acumulados perto da ponte.', 'Igarapé do Mindu'),
    (4, -3.1307664, -59.9964426, '2026-08-28 16:20:00', NULL, 'Vidro', 'Medio', 'Nova', 'Garrafas de vidro quebradas.', 'Igarapé do Quarenta');
