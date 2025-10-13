# db_init.py
import sqlite3

DB_FILE = "bot.db"

def init_db():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    # Tabela de alunos
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS usuarios (
            user_id INTEGER PRIMARY KEY AUTOINCREMENT,
            matricula TEXT UNIQUE NOT NULL,
            nome TEXT NOT NULL
        )
    """)
    # Tabela de notas
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS notas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            disciplina TEXT NOT NULL,
            nota REAL NOT NULL,
            FOREIGN KEY(user_id) REFERENCES usuarios(user_id)
        )
    """)
    conn.commit()
    conn.close()

if __name__ == "__main__":
    init_db()
