from flask import Flask, render_template, request, redirect, url_for, g
import sqlite3

app = Flask(__name__)


db_name = 'database.db'

# Função para criar a tabela
def create_table():
    conn = sqlite3.connect(db_name)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS pessoa
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, nome TEXT, cpf TEXT)''')
    conn.commit()
    conn.close()

@app.route('/')
def index():
  conn = sqlite3.connect(db_name)
  cursor = conn.cursor()
  sqlSELECT = "SELECT * FROM pessoa"
  cursor.execute(sqlSELECT)
  pessoas = cursor.fetchall()
  conn.close()
  return render_template('index.html', pessoas=pessoas)
# Rota para cadastrar uma nova pessoa

@app.route('/cadastrar', methods=['POST'])
def cadastrar_pessoa():
   conn = sqlite3.connect(db_name)
   cursor = conn.cursor()
   cursor.execute("INSERT INTO pessoa (nome, cpf) VALUES (?, ?)", (request.form['nome'], request.form['cpf']))
   conn.commit()
   conn.close()
   return redirect(url_for('index'))

# Rota para editar uma pessoa
@app.route('/editar/<int:id>', methods=['GET', 'POST'])
def editar_pessoa(id):
      conn = sqlite3.connect(db_name)
      cursor = conn.cursor()
      if request.method == "POST":
        cursor.execute("UPDATE pessoa SET nome=?, cpf=? WHERE id=?",(request.form['nome'],request.form['cpf'],id))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))
      else:
        cursor.execute("SELECT * FROM pessoa WHERE id=?", (id,))
        pessoa = cursor.fetchone()
        conn.close()
        return render_template('editar.html', pessoa=pessoa)

# Rota para excluir uma pessoa
@app.route('/excluir/<int:id>')
def excluir_pessoa(id):
  conn = sqlite3.connect(db_name)
  cursor = conn.cursor()
  sqlDelete = "DELETE FROM pessoa WHERE id = ?"
  cursor.execute(sqlDelete, (id, ))
  conn.commit()
  conn.close()
  return redirect(url_for('index'))

if __name__ == "__main__":
    create_table()
    app.run(host="0.0.0.0", port=5000, debug=True, use_reloader=True)
