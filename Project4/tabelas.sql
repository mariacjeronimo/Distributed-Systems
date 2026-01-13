-- """
-- Aplicações Distribuídas - Projeto 3 - tabelas.sql
-- Grupo: 23
-- Números de aluno: Maria Jerónimo 56887, Lara Ângelo 56945
-- """

PRAGMA foreign_keys = ON;

CREATE TABLE utilizadores (
    id INTEGER PRIMARY KEY,
    nome TEXT,
    senha TEXT
);

CREATE TABLE musicas (
    id INTEGER PRIMARY KEY,
    id_spotify TEXT,
    nome TEXT,
    id_artista INTEGER,
    FOREIGN KEY(id_artista) REFERENCES artistas(id) ON DELETE CASCADE
);

CREATE TABLE artistas (
    id INTEGER PRIMARY KEY,
    id_spotify TEXT,
    nome TEXT
);

CREATE TABLE avaliacoes (
    id INTEGER PRIMARY KEY,
    sigla TEXT,
    designacao TEXT
);

CREATE TABLE playlists (
    id_user INTEGER,
    id_musica INTEGER,
    id_avaliacao INTEGER,
    PRIMARY KEY (id_user, id_musica),
    FOREIGN KEY(id_user) REFERENCES utilizadores(id) ON DELETE CASCADE,
    FOREIGN KEY(id_musica) REFERENCES musicas(id) ON DELETE CASCADE,
    FOREIGN KEY(id_avaliacao) REFERENCES avaliacoes(id) ON DELETE CASCADE
);

INSERT INTO avaliacoes (id, sigla, designacao) VALUES
(1, "M", "Medíocre"),
(2, "m", "Mau"),
(3, "S", "Suficiente"),
(4, "B", "Boa"),
(5, "MB", "Muito Boa")
;