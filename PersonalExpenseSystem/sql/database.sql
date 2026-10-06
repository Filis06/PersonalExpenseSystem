-- ============================================================================
-- 1. ABILITAZIONE DEI VINCOLI DI INTEGRITÀ REFERENZIALE
-- ============================================================================
PRAGMA foreign_keys = ON;

-- ============================================================================
-- 2. CREAZIONE DELLE TABELLE E DEFINIZIONE DEI VINCOLI
-- ============================================================================

-- Creazione della Tabella CATEGORIE
CREATE TABLE CATEGORIE (
    PK_id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome_categoria TEXT NOT NULL UNIQUE CHECK (length(trim(nome_categoria)) > 0)
);

-- Creazione della Tabella SPESE
CREATE TABLE SPESE (
    PK_id INTEGER PRIMARY KEY AUTOINCREMENT,
    data TEXT NOT NULL CHECK (data LIKE '____-__-__'), -- Forza il formato YYYY-MM-DD
    importo REAL NOT NULL CHECK (importo > 0),         -- Vincolo CHECK: importo maggiore di zero
    descrizione TEXT,
    FK_id_categoria INTEGER NOT NULL,
    FOREIGN KEY (FK_id_categoria) REFERENCES CATEGORIE(PK_id) ON DELETE RESTRICT
);

-- Creazione della Tabella BUDGET
CREATE TABLE BUDGET (
    PK_id INTEGER PRIMARY KEY AUTOINCREMENT,
    mese TEXT NOT NULL CHECK (mese LIKE '____-__'),    -- Forza il formato YYYY-MM
    importo_budget REAL NOT NULL CHECK (importo_budget > 0), -- Vincolo CHECK: budget maggiore di zero
    FK_id_categoria INTEGER NOT NULL,
    FOREIGN KEY (FK_id_categoria) REFERENCES CATEGORIE(PK_id) ON DELETE RESTRICT,
    UNIQUE(mese, FK_id_categoria) -- Impedisce doppi budget per la stessa categoria nello stesso mese
);

-- ============================================================================
-- 3. INSERIMENTO DATI DI ESEMPIO (POPOLAMENTO INIZIALE)
-- ============================================================================

INSERT INTO CATEGORIE (nome_categoria) VALUES ('Alimentari');
INSERT INTO CATEGORIE (nome_categoria) VALUES ('Trasporti');
INSERT INTO CATEGORIE (nome_categoria) VALUES ('Intrattenimento');

INSERT INTO SPESE (data, importo, descrizione, FK_id_categoria) VALUES ('2026-11-01', 25.50, 'Spesa supermercato', 1);
INSERT INTO SPESE (data, importo, descrizione, FK_id_categoria) VALUES ('2026-11-02', 15.00, 'Ricarica abbonamento bus', 2);

INSERT INTO BUDGET (mese, importo_budget, FK_id_categoria) VALUES ('2026-11', 200.00, 1);
INSERT INTO BUDGET (mese, importo_budget, FK_id_categoria) VALUES ('2026-11', 50.00, 2);

