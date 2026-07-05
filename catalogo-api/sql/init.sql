-- =============================================
-- Sistema de Biblioteca
-- Script de criação das tabelas
-- =============================================

CREATE TABLE IF NOT EXISTS livro (
    id                    SERIAL PRIMARY KEY,
    titulo                VARCHAR(255) NOT NULL,
    autor                 VARCHAR(255) NOT NULL,
    ano_publicacao        INTEGER,
    isbn                  VARCHAR(20) UNIQUE,
    quantidade_total      INTEGER NOT NULL DEFAULT 1 CHECK (quantidade_total >= 0),
    quantidade_disponivel INTEGER NOT NULL DEFAULT 1 CHECK (quantidade_disponivel >= 0)
);

CREATE TABLE IF NOT EXISTS socio (
    id             SERIAL PRIMARY KEY,
    nome           VARCHAR(255) NOT NULL,
    email          VARCHAR(255) UNIQUE NOT NULL,
    telefone       VARCHAR(20),
    data_cadastro  DATE NOT NULL DEFAULT CURRENT_DATE
);

CREATE TABLE IF NOT EXISTS emprestimo (
    id                      SERIAL PRIMARY KEY,
    livro_id                INTEGER NOT NULL REFERENCES livro(id),
    socio_id                INTEGER NOT NULL REFERENCES socio(id),
    data_emprestimo         DATE NOT NULL DEFAULT CURRENT_DATE,
    data_prevista_devolucao DATE NOT NULL,
    data_devolucao          DATE,
    status                  VARCHAR(20) NOT NULL DEFAULT 'aberto'
        CHECK (status IN ('aberto', 'devolvido'))
);

-- Índices para buscas frequentes
CREATE INDEX IF NOT EXISTS idx_emprestimo_livro  ON emprestimo(livro_id);
CREATE INDEX IF NOT EXISTS idx_emprestimo_socio  ON emprestimo(socio_id);
CREATE INDEX IF NOT EXISTS idx_emprestimo_status ON emprestimo(status);
