from flask import Flask, render_template, request, redirect, url_for,flash
from werkzeug.security import generate_password_hash, check_password_hash

import mysql.connector

app = Flask(__name__)
app.secret_key = "chave_secreta"


# Configurações do banco
db_config = {
    "host": "localhost",
    "user": "root",
    "password": "659326@#Te"
}


# Cria a base de dados
def create_database():
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        cursor.execute("CREATE DATABASE IF NOT EXISTS projeto")
        print("Banco de dados criado (ou já existia).")
        cursor.close()
        conn.close()
    except Exception as e:
        print("Erro ao criar banco:", e)
        

#Criando a tabela no banco    
def create_tables():
  try:
      conn = mysql.connector.connect(
              host=db_config["host"],
              user=db_config["user"],
              password=db_config["password"],
              database="projeto"
)
      cursor = conn.cursor()  
      cursor.execute("""
        CREATE TABLE IF NOT EXISTS usuarios (
            id INT AUTO_INCREMENT PRIMARY KEY,
            nome VARCHAR(100) NOT NULL,
            email VARCHAR(100) NOT NULL UNIQUE,
            senha VARCHAR(100) NOT NULL
        )
    """)
      print("Tabela 'usuarios' criada (ou já existia).")
      cursor.close()
      conn.close()
  except Exception as e:
      print("Erro ao criar tabela:", e)

create_database() 
create_tables()

db = mysql.connector.connect(
    host=db_config["host"],
    user=db_config["user"],
    password=db_config["password"],
    database="projeto"
)
cursor = db.cursor()

############################ROTAS########################################


# Rota de Registro
@app.route('/register')
def register():
    return render_template('registro.html')

# Rota de novo usuario
@app.route('/new_user', methods=['POST'])
def add_user():
    nome = request.form['usuario']
    email = request.form['email']
    senha = request.form['senha']
    check_senha = request.form['check_senha']
    
    if senha!=check_senha:
      flash("As senhas não coincidem!", "erro")
      return render_template("registro.html",nome=nome, email=email)
      
    senha_hash = generate_password_hash(senha)
    try:
      cursor.execute("INSERT INTO usuarios (nome,email,senha) VALUES (%s, %s,%s)", (nome,email,senha_hash))
      db.commit()
      flash("Usuário cadastrado com sucesso!", "sucesso")
      return render_template('login.html')
    except mysql.connector.IntegrityError:
      flash ("Erro: email já cadastrado!")
      return render_template("registro.html", nome=nome, email=email)
    
    
# Rota de login
@app.route('/')
def home():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    email = request.form['email']
    senha = request.form['senha']
    
    cursor.execute("SELECT * FROM usuarios WHERE email=%s", (email,))
    user = cursor.fetchone()

    if user and check_password_hash(user[3], senha):  
      return render_template('home.html', nome=user[1])
    else:
      return "Usuário ou senha incorretos!"


if __name__ == "__main__":
    app.run(debug=True)


