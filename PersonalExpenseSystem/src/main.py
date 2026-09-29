import sqlite3

DB_NAME = "spese_personali.db"

def inizializza_database():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("PRAGMA foreign_keys = ON;")
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Categorie (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome_categoria TEXT NOT NULL UNIQUE CHECK(length(trim(nome_categoria)) > 0)
    );
    """)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Spese (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        data TEXT NOT NULL CHECK(data LIKE '____-__-__'),
        importo REAL NOT NULL CHECK(importo > 0),
        descrizione TEXT,
        id_categoria INTEGER NOT NULL,
        FOREIGN KEY (id_categoria) REFERENCES Categorie(id) ON DELETE RESTRICT
    );
    """)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Budget (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        mese TEXT NOT NULL CHECK(mese LIKE '____-__'),
        importo_budget REAL NOT NULL CHECK(importo_budget > 0),
        id_categoria INTEGER NOT NULL,
        FOREIGN KEY (id_categoria) REFERENCES Categorie(id) ON DELETE RESTRICT,
        UNIQUE(mese, id_categoria)
    );
    """)
    cursor.execute("SELECT COUNT(*) FROM Categorie;")
    if cursor.fetchone()[0] == 0:
        cursor.execute("INSERT INTO Categorie (nome_categoria) VALUES ('Alimentari');")
        cursor.execute("INSERT INTO Categorie (nome_categoria) VALUES ('Trasporti');")
        cursor.execute("INSERT INTO Spese (data, importo, descrizione, id_categoria) VALUES ('2026-11-01', 25.50, 'Spesa supermercato', 1);")
        cursor.execute("INSERT INTO Budget (mese, importo_budget, id_categoria) VALUES ('2026-11', 200.00, 1);")
    conn.commit()
    conn.close()

def gestione_categorie():
    print("\n--- MODULO 1 — Gestione delle Categorie ---")
    nome = input("Inserisci il nome della categoria: ").strip()
    if not nome:
        print("Errore: Il nome non può essere vuoto.")
        return
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM Categorie WHERE LOWER(nome_categoria) = LOWER(?);", (nome,))
    if cursor.fetchone():
        print("La categoria esiste già.")
    else:
        cursor.execute("INSERT INTO Categorie (nome_categoria) VALUES (?);", (nome,))
        conn.commit()
        print("Categoria inserita correttamente.")
    conn.close()

def inserisci_spesa():
    print("\n--- MODULO 2 — Inserimento di una Spesa ---")
    data = input("Data (YYYY-MM-DD): ").strip()
    try:
        importo = float(input("Importo: "))
    except ValueError:
        print("Errore: importo non valido.")
        return
    if importo <= 0:
        print("Errore: deve essere maggiore di zero.")
        return
    nome_cat = input("Nome della categoria: ").strip()
    descrizione = input("Descrizione facoltativa: ").strip()
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM Categorie WHERE LOWER(nome_categoria) = LOWER(?);", (nome_cat,))
    row = cursor.fetchone()
    if not row:
        print("Errore: la categoria non esiste.")
    else:
        cursor.execute("INSERT INTO Spese (data, importo, descrizione, id_categoria) VALUES (?, ?, ?, ?);", 
                       (data, importo, descrizione if descrizione else None, row[0]))
        conn.commit()
        print("Spesa inserita correttamente.")
    conn.close()

def definisci_budget():
    print("\n--- MODULO 3 — Definizione del Budget Mensile ---")
    mese = input("Mese (YYYY-MM): ").strip()
    nome_cat = input("Nome della categoria: ").strip()
    try:
        importo_budget = float(input("Importo del budget: "))
    except ValueError:
        print("Errore: importo non valido.")
        return
    if importo_budget <= 0:
        print("Errore: deve essere maggiore di zero.")
        return
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM Categorie WHERE LOWER(nome_categoria) = LOWER(?);", (nome_cat,))
    row = cursor.fetchone()
    if not row:
        print("Errore: la categoria non esiste.")
    else:
        cursor.execute("INSERT OR REPLACE INTO Budget (mese, importo_budget, id_categoria) VALUES (?, ?, ?);", (mese, importo_budget, row[0]))
        conn.commit()
        print("Budget salvato correttamente.")
    conn.close()

def visualizza_report():
    while True:
        print("\n--- MENU REPORT ---")
        print("1. Totale spese per categoria\n2. Spese vs budget\n3. Elenco completo spese\n4. Torna al menu principale")
        scelta = input("Scelta: ").strip()
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        if scelta == "1":
            cursor.execute("SELECT C.nome_categoria, IFNULL(SUM(S.importo), 0) FROM Categorie C LEFT JOIN Spese S ON C.id = S.id_categoria GROUP BY C.nome_categoria;")
            for row in cursor.fetchall():
                print(f"{row[0]}: {row[1]:.2f}")
        elif scelta == "2":
            cursor.execute("SELECT B.mese, C.nome_categoria, B.importo_budget, IFNULL(SUM(S.importo), 0) FROM Budget B JOIN Categorie C ON B.id_categoria = C.id LEFT JOIN Spese S ON C.id = S.id_categoria AND STRFTIME('%Y-%m', S.data) = B.mese GROUP BY B.mese, B.id_categoria;")
            for row in cursor.fetchall():
                print(f"\nMese: {row[0]}\nCategoria: {row[1]}\nBudget: {row[2]:.2f}\nSpeso: {row[3]:.2f}")
                if row[3] > row[2]: print("Stato: SUPERAMENTO BUDGET")
        elif scelta == "3":
            cursor.execute("SELECT S.data, C.nome_categoria, S.importo, IFNULL(S.descrizione, '') FROM Spese S JOIN Categorie C ON S.id_categoria = C.id ORDER BY S.data ASC;")
            for row in cursor.fetchall():
                print(f"{row[0]} | {row[1]} | {row[2]:.2f} | {row[3]}")
        elif scelta == "4":
            conn.close()
            break
        conn.close()

def main():
    inizializza_database()
    print("Benvenuto nel Sistema di Gestione delle Spese Personali!")
    while True:
        print("\n--- MENU PRINCIPALE ---")
        print("1. Gestione Categorie\n2. Inserisci Spesa\n3. Definisci Budget Mensile\n4. Visualizza Report\n5. Esci")
        scelta = input("Inserisci la tua scelta: ").strip()
        if scelta == "1": gestione_categorie()
        elif scelta == "2": inserisci_spesa()
        elif scelta == "3": definisci_budget()
        elif scelta == "4": visualizza_report()
        elif scelta == "5":
            print("Arrivederci!")
            break

# Avvio diretto del programma senza costrutti condizionali
main()
