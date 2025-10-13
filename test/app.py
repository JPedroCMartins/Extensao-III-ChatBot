# app.py
from flask import Flask, render_template, request, redirect, url_for
import sqlite3

DB_FILE = "bot.db"
app = Flask(__name__)

# --- Rotas ---
@app.route("/")
def index():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM usuarios")
    alunos = cursor.fetchall()
    conn.close()
    return render_template("index.html", alunos=alunos)

@app.route("/add_aluno", methods=["POST"])
def add_aluno():
    nome = request.form.get("nome")
    matricula = request.form.get("matricula")
    if nome and matricula:
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        cursor.execute("INSERT OR IGNORE INTO usuarios (matricula, nome) VALUES (?, ?)", (matricula, nome))
        conn.commit()
        conn.close()
    return redirect(url_for("index"))

@app.route("/aluno/<int:user_id>")
def aluno(user_id):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT nome, matricula FROM usuarios WHERE user_id=?", (user_id,))
    aluno = cursor.fetchone()

    cursor.execute("SELECT * FROM notas WHERE user_id=?", (user_id,))
    notas = cursor.fetchall()
    conn.close()
    return render_template("aluno.html", aluno=aluno, notas=notas, user_id=user_id)

@app.route("/add_nota/<int:user_id>", methods=["POST"])
def add_nota(user_id):
    disciplina = request.form.get("disciplina")
    nota = request.form.get("nota")
    if disciplina and nota:
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO notas (user_id, disciplina, nota) VALUES (?, ?, ?)",
                       (user_id, disciplina, float(nota)))
        conn.commit()
        conn.close()
    return redirect(url_for("aluno", user_id=user_id))

if __name__ == "__main__":
    app.run(debug=True)
