PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS ocorrencias (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    latitude REAL NOT NULL,
    longitude REAL NOT NULL,
    data_hora TEXT NOT NULL DEFAULT (datetime('now')),
    fotografia TEXT,
    tipo_residuo TEXT NOT NULL,
    nivel_acumulo TEXT NOT NULL,
    observacoes TEXT,
    local_nome TEXT
);

CREATE INDEX IF NOT EXISTS idx_ocorrencias_coord
ON ocorrencias (latitude, longitude);

INSERT INTO ocorrencias
    (latitude, longitude, data_hora, fotografia, tipo_residuo, nivel_acumulo, observacoes, local_nome)
VALUES
    (-3.059860, -60.040980, '2026-08-24 09:15:00', NULL, 'Plastico', 'Alto', 'Acúmulo grande próximo às margens, muitos sacos plásticos.', 'Igarapé do Mindu'),
    (-3.058412, -60.045120, '2026-08-25 14:30:00', NULL, 'Misto', 'Medio', 'Garrafas pet e embalagens espalhadas.', 'Igarapé do Mindu'),
    (-3.061230, -60.038500, '2026-08-26 10:05:00', NULL, 'Metal', 'Baixo', 'Poucas latas e ferros velhos.', 'Igarapé do Mindu'),
    (-3.063900, -60.042300, '2026-08-27 11:45:00', NULL, 'Organico', 'Alto', 'Resíduos orgânicos acumulados perto da ponte.', 'Igarapé do Mindu'),
    (-3.057500, -60.047000, '2026-08-28 16:20:00', NULL, 'Vidro', 'Medio', 'Garrafas de vidro quebradas.', 'Igarapé do Mindu');
