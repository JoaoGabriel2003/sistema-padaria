from flask import Flask, render_template, request, redirect, url_for, session
from banco import conectar_bd
from werkzeug.security import check_password_hash
from werkzeug.security import generate_password_hash
import secrets
import sqlite3

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)

# Página inicial
@app.route('/')
def index():
    return render_template('index.html')

# Redefinir senha
@app.route('/redefinir_senha', methods=['GET', 'POST'])
def redefinir_senha():
    mensagem = None
    erro = None

    if request.method == 'POST':
        usuario = request.form['usuario']
        nova_senha = request.form['nova_senha']
        nova_senha_hash = generate_password_hash(nova_senha)

        conn = conectar_bd()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM usuarios WHERE usuario=?", (usuario,))
        if cursor.fetchone():
            cursor.execute("UPDATE usuarios SET senha=? WHERE usuario=?", (nova_senha_hash, usuario))
            conn.commit()
            mensagem = "Senha redefinida com sucesso!"
        else:
            erro = "Usuário não encontrado!"
        conn.close()

    return render_template('redefinir_senha.html', mensagem=mensagem, erro=erro)



# Registro de usuário
@app.route('/registrar', methods=['GET', 'POST'])
def registrar():
    erro = None
    if request.method == 'POST':
        usuario = request.form['usuario']
        senha = request.form['senha']

        conn = conectar_bd()
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM usuarios WHERE usuario=?", (usuario,))
        if cursor.fetchone():
            erro = 'Usuário já existe!'
        else:
            senha_hash = generate_password_hash(senha)
            cursor.execute("INSERT INTO usuarios (usuario, senha) VALUES (?, ?)", (usuario, senha_hash))
            conn.commit()
            conn.close()
            return redirect(url_for('login'))

        conn.close()

    return render_template('registrar.html', erro=erro)


# Login
@app.route('/login', methods=['GET', 'POST'])
def login():
    erro = None
    if request.method == 'POST':
        usuario = request.form['usuario']
        senha = request.form['senha']

        conn = conectar_bd()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM usuarios WHERE usuario=?", (usuario,))
        usuario_encontrado = cursor.fetchone()
        conn.close()

        if usuario_encontrado and check_password_hash(usuario_encontrado[2], senha):
            session['usuario'] = usuario
            return redirect(url_for('index'))
        else:
            erro = 'Usuário ou senha inválidos!'

    return render_template('login.html', erro=erro)


# Logout
@app.route('/logout')
def logout():
    session.pop('usuario', None)
    return redirect(url_for('login', logout=1))

# Produtos (listagem com filtro e ordenação)
@app.route('/produtos')
def produtos():
    if 'usuario' not in session:
        return redirect(url_for('login'))

    busca = request.args.get('busca', '')
    categoria = request.args.get('categoria', '')
    order_by = request.args.get('order_by', 'id')

    conn = conectar_bd()
    cursor = conn.cursor()

    query = "SELECT * FROM produtos"
    filtros = []
    params = []

    if busca:
        filtros.append("nome LIKE ?")
        params.append(f"%{busca}%")
    if categoria:
        filtros.append("categoria = ?")
        params.append(categoria)

    if filtros:
        query += " WHERE " + " AND ".join(filtros)

    if order_by in ['id', 'nome', 'categoria', 'preco', 'quantidade']:
        query += f" ORDER BY {order_by}"

    cursor.execute(query, params)
    produtos = cursor.fetchall()
    conn.close()

    return render_template('produtos.html', produtos=produtos, busca=busca, categoria=categoria)

# Cadastrar novo produto
@app.route('/cadastrar', methods=['GET', 'POST'])
def cadastrar():
    if 'usuario' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        nome = request.form['nome']
        categoria = request.form['categoria']
        preco = request.form['preco']
        quantidade = request.form['quantidade']

        conn = conectar_bd()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO produtos (nome, categoria, preco, quantidade) VALUES (?, ?, ?, ?)",
            (nome, categoria, preco, quantidade)
        )
        conn.commit()
        conn.close()

        return redirect(url_for('produtos'))

    return render_template('cadastrar.html')

# Editar produto
@app.route('/editar/<int:id>', methods=['GET', 'POST'])
def editar(id):
    if 'usuario' not in session:
        return redirect(url_for('login'))

    conn = conectar_bd()
    cursor = conn.cursor()

    if request.method == 'POST':
        nome = request.form['nome']
        categoria = request.form['categoria']
        preco = request.form['preco']
        quantidade = request.form['quantidade']

        cursor.execute(
            "UPDATE produtos SET nome=?, categoria=?, preco=?, quantidade=? WHERE id=?",
            (nome, categoria, preco, quantidade, id)
        )
        conn.commit()
        conn.close()
        return redirect(url_for('produtos'))

    cursor.execute("SELECT * FROM produtos WHERE id=?", (id,))
    produto = cursor.fetchone()
    conn.close()

    return render_template('editar.html', produto=produto)

# Excluir produto
@app.route('/excluir/<int:id>')
def excluir(id):
    if 'usuario' not in session:
        return redirect(url_for('login'))

    conn = conectar_bd()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM produtos WHERE id=?", (id,))
    conn.commit()
    conn.close()

    return redirect(url_for('produtos'))

# Executa o app
if __name__ == '__main__':
    app.run(debug=True)
