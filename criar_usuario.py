import sqlite3
from werkzeug.security import generate_password_hash  # Adiciona isso

# Conectar ao banco existente
conexao = sqlite3.connect('padaria.db')
cursor = conexao.cursor()

# Criar tabela de usuários (só se ainda não existir)
cursor.execute('''
CREATE TABLE IF NOT EXISTS usuarios (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    usuario TEXT NOT NULL UNIQUE,
    senha TEXT NOT NULL
)
''')

# Inserir novo usuário
usuario = 'admin'
senha_plana = '1234'
senha = generate_password_hash(senha_plana)  # Criptografa a senha

try:
    cursor.execute("INSERT INTO usuarios (usuario, senha) VALUES (?, ?)", (usuario, senha))
    conexao.commit()
    print("Usuário criado com sucesso!")
except sqlite3.IntegrityError:
    print("Usuário já existe!")

conexao.close()
