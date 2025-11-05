from flask import Flask, render_template, request, redirect, url_for,flash
from werkzeug.security import generate_password_hash, check_password_hash

import mysql.connector

app = Flask(__name__)
app.secret_key = "chave_secreta";


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
            senha LONGTEXT NOT NULL
        )
    """)
      
      cursor.execute("""
        CREATE TABLE IF NOT EXISTS clientes (
            id INT AUTO_INCREMENT PRIMARY KEY,
            nome VARCHAR(100) NOT NULL,
            email VARCHAR(100) NOT NULL UNIQUE,
            endereco VARCHAR(100) NOT NULL,
            telefone  VARCHAR(100) NOT NULL
        )
    """)
      cursor.execute("""
        CREATE TABLE IF NOT EXISTS barbeiros (
            id INT AUTO_INCREMENT PRIMARY KEY,
            nome VARCHAR(100) NOT NULL,
            email VARCHAR(100) NOT NULL UNIQUE,
            endereco VARCHAR(100) NOT NULL,
            telefone  VARCHAR(100) NOT NULL
        )
    """)
      cursor.execute("""
    CREATE TABLE IF NOT EXISTS barbeiro_servicos (
        id INT AUTO_INCREMENT PRIMARY KEY,
        barbeiro_id INT NOT NULL,
        servico VARCHAR(50) NOT NULL,
        FOREIGN KEY (barbeiro_id) REFERENCES barbeiros(id) ON DELETE CASCADE
    )
""")

      print("Tabela 'usuarios' criada (ou já existia)."),
      print("Tabela 'clientes' criada (ou já existia).")
      print("Tabela 'barbeiro' criada (ou já existia).")
      print("Tabela 'barbeiro_servicos' criada (ou já existia).")
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
    
# >>>>>>>>>>>>>>>>>>>>>>>>>USUARISOS SISTEMA<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<

# Rota de Registro
@app.route('/register')
def register():
    return render_template('registroUsuario.html')

# Rota de novo usuario
@app.route('/new_user', methods=['POST'])
def add_user():
    nome = request.form['usuario']
    email = request.form['email']
    senha = request.form['senha']
    check_senha = request.form['check_senha']
    
    if senha!=check_senha:
      flash("As senhas não coincidem!", "erro")
      return render_template("registroUsuario.html",nome=nome, email=email)
      
    senha_hash = generate_password_hash(senha)
    try:
      cursor.execute("INSERT INTO usuarios (nome,email,senha) VALUES (%s, %s,%s)", (nome,email,senha_hash))
      db.commit()
      flash("Usuário cadastrado com sucesso!", "sucesso")
      return render_template('login.html')
    except mysql.connector.IntegrityError:
      flash ("Erro: email já cadastrado!")
      return render_template("registroUsuario.html", nome=nome, email=email)
    
    
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
    
# >>>>>>>>>>>>>>>>>>>>>>>>>CLIENTES<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<


@app.route('/voltarHome')
def voltarHome():
    return render_template('home.html')

# Rota de novo Cliente
@app.route('/cliente')
def cliente():
    return render_template('cadastroCliente.html')
  
#ROTA INCLUI
@app.route('/incluir')
def incluir():
    return render_template('incluiClientes.html') 
  

@app.route('/incluiCliente', methods=['POST'])
def incluiCliente():
    nome = request.form['nome']
    endereco = request.form['endereco']
    email = request.form['email']
    telefone = request.form['telefone']
    
    try:
      cursor.execute("INSERT INTO clientes (nome,endereco,email,telefone) VALUES (%s, %s,%s,%s)", (nome,endereco,email,telefone))
      db.commit()
      flash("Cliente cadastrado com sucesso!", "sucesso")
      return render_template('cadastroCliente.html')
    except mysql.connector.IntegrityError:
      flash ("Erro: email já cadastrado!")
      return render_template("incluiClientes.html", nome=nome, email=email)
    

    
# Rota Listar Cliente
@app.route('/listarCliente')
def listarCliente():
  return render_template ('buscarCliente.html')
    
#ROTA BUSCAR
@app.route('/buscar_Cliente', methods = ['POST']) 
def buscarCliente():
  
  nome = request.form.get('nome','')
  email = request.form.get('email','')
  
  conn = mysql.connector.connect(
        host=db_config["host"],
        user=db_config["user"],
        password=db_config["password"],
        database="projeto"     
  )
  cursor = conn.cursor(dictionary=True)
   
  query = """
        SELECT id, nome, email, endereco, telefone
        FROM clientes
        WHERE nome LIKE %s OR email LIKE %s
    """

  cursor.execute(query, (f"%{nome}%", f"%{email}%"))
  clientes = cursor.fetchall()
  
  cursor.close()
  
  if not clientes:
        flash("Nenhum cliente encontrado!", "erro")
        return render_template('buscarCliente.html', clientes=clientes)
  
  return render_template("clientes.html", clientes=clientes or [])

#ROTA EDITAR
@app.route('/editarCliente/<int:id>', methods=['GET', 'POST'])
def editarCliente(id):
    if request.method == 'GET':
        cursor.execute("SELECT * FROM clientes WHERE id = %s", (id,))
        cliente = cursor.fetchone()
        return render_template('incluiClientes.html', cliente=cliente)
    else:
        nome = request.form['nome']
        email = request.form['email']
        endereco = request.form['endereco']
        telefone = request.form['telefone']
        cursor.execute("""
            UPDATE clientes 
            SET nome=%s, email=%s, endereco=%s, telefone=%s 
            WHERE id=%s
        """, (nome, email, endereco, telefone, id))
        db.commit()
        flash("Cliente atualizado com sucesso!", "success")
    
    return render_template('cadastroCliente.html')

#ROTA EXCLUI
@app.route('/excluirCliente/<int:id>', methods=['POST'])
def excluirCliente(id):
    try:
        cursor.execute("DELETE FROM clientes WHERE id = %s", (id,))
        db.commit()
        flash("Cliente excluído com sucesso!", "success")
    except Exception as e:
        db.rollback()
        flash(f"Erro ao excluir cliente: {e}", "error")
    return render_template('buscarCliente.html')
  

# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>Barbeiro<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<

# Rota de novo Barbeiro
@app.route('/barbeiro')
def barbeiro():
    return render_template('cadastroBarbeiro.html')
  
#ROTA INCLUI
@app.route('/incluirB')
def incluirB():
    return render_template('incluiBarbeiro.html') 
  

@app.route('/incluiBarbeiro', methods=['POST'])
def incluiBarbeiro():
    nome = request.form['nome']
    endereco = request.form['endereco']
    email = request.form['email']
    telefone = request.form['telefone']
    servicos = request.form.getlist('servicos')
    
    
    try:
      cursor.execute("INSERT INTO barbeiros (nome,endereco,email,telefone) VALUES (%s, %s,%s,%s)", (nome,endereco,email,telefone))
      db.commit()
      barbeiro_id = cursor.lastrowid
      for servico in servicos:
            cursor.execute(
                "INSERT INTO barbeiro_servicos (barbeiro_id, servico) VALUES (%s, %s)",
                (barbeiro_id, servico)
            )
      db.commit()
      flash("Barbeiro cadastrado com sucesso!", "sucesso")
      return render_template('cadastroBarbeiro.html')
    
    except mysql.connector.IntegrityError:
      flash ("Erro: email já cadastrado!")
      return render_template("incluiBarbeiro.html", nome=nome, email=email)
    
    except Exception as e:
        db.rollback()
        flash(f"Erro ao cadastrar barbeiro: {e}", "erro")
        return render_template("incluiBarbeiro.html", nome=nome, email=email)
    
# Rota Listar Barbeiro
@app.route('/listarBarbeiro')
def listarBarbeiro():
  return render_template ('buscarBarbeiro.html')
    
#ROTA BUSCAR
@app.route('/buscar_Barbeiro', methods = ['POST']) 
def buscarBarbeiro():
  
  nome = request.form.get('nome','')
  email = request.form.get('email','')
  try:
    conn = mysql.connector.connect(
        host=db_config["host"],
        user=db_config["user"],
        password=db_config["password"],
        database="projeto"     
    )
    cursor = conn.cursor(dictionary=True)
   
    query = """
        SELECT id, nome, email, endereco, telefone
        FROM barbeiros
        WHERE nome LIKE %s OR email LIKE %s
    """

    cursor.execute(query, (f"%{nome}%", f"%{email}%"))
    barbeiros = cursor.fetchall()
  
  
  
    if not barbeiros:
        flash("Nenhum profissional encontrado!", "erro")  
        return render_template('buscarBarbeiro.html')
      
      
    for b in barbeiros:
      cursor.execute("""
          SELECT servico FROM barbeiro_servicos WHERE barbeiro_id = %s
        """, (b['id'],))
      servicos = [s['servico'] for s in cursor.fetchall()]
      b['servicos'] = ', '.join(servicos) if servicos else 'Nenhum serviço cadastrado'

  
    return render_template("barbeiro.html",  barbeiros=barbeiros);
  except Exception as e:
        flash(f"Erro ao buscar barbeiros: {e}", "erro")
        return render_template('buscarBarbeiro.html')

  finally:
        # Fecha o cursor e a conexão se existirem
        try:
            if cursor:
                cursor.close()
            if conn:
                conn.close()
        except:
            pass

#ROTA EDITAR
@app.route('/editarBarbeiro/<int:id>', methods=['GET', 'POST'])
def editarBarbeiro(id):
    if request.method == 'GET':
        cursor.execute("SELECT * FROM barbeiros WHERE id = %s", (id,))
        barbeiro = cursor.fetchone()
        
        
        cursor.execute("SELECT servico FROM barbeiro_servicos WHERE barbeiro_id = %s", (id,))
        servicos_barbeiro = [row[0] for row in cursor.fetchall()] 
        return render_template('incluiBarbeiro.html', barbeiro=barbeiro, servicos_barbeiro=servicos_barbeiro)
    else:
        nome = request.form['nome']
        email = request.form['email']
        endereco = request.form['endereco']
        telefone = request.form['telefone']
        servicos = request.form.getlist('servicos')
        try:
          cursor.execute("""
            UPDATE barbeiros 
            SET nome=%s, email=%s, endereco=%s, telefone=%s 
            WHERE id=%s
        """, (nome, email, endereco, telefone, id))
          db.commit()
        
        
          cursor.execute("DELETE FROM barbeiro_servicos WHERE barbeiro_id = %s", (id,))

     
          for servico in servicos:
                cursor.execute(
                    "INSERT INTO barbeiro_servicos (barbeiro_id, servico) VALUES (%s, %s)",
                    (id, servico)
                )
          db.commit()
        
          flash("Profissional atualizado com sucesso!", "success")
          return render_template('cadastroBarbeiro.html')
      
        except Exception as e:
            db.rollback()
            flash(f"Erro ao atualizar barbeiro: {e}", "error")
            return render_template('incluiBarbeiro.html', barbeiro=barbeiro)

#ROTA EXCLUI
@app.route('/excluirBarbeiro/<int:id>', methods=['POST'])
def excluirBarbeiro(id):
    try:
        cursor.execute("DELETE FROM barbeiros WHERE id = %s", (id,))
        db.commit()
        flash("Profissional excluído com sucesso!", "success")
    except Exception as e:
        db.rollback()
        flash(f"Erro ao excluir profissional: {e}", "error")
    return render_template('buscarBarbeiro.html')
  

 
if __name__ == "__main__":
    app.run(debug=True)


