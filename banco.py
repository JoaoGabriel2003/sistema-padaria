import sqlite3

def conectar_bd():
    conexao = sqlite3.connect('padaria.db')
    return conexao

# Cria o banco (ou conecta se já existir)
conexao = sqlite3.connect('padaria.db')
cursor = conexao.cursor()

# Cria a tabela de produtos
cursor.execute('''
    CREATE TABLE IF NOT EXISTS produtos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        categoria TEXT,
        preco REAL,
        quantidade INTEGER
    )
''')

# Cria a tabela de usuários
cursor.execute('''
    CREATE TABLE IF NOT EXISTS usuarios (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        usuario TEXT NOT NULL UNIQUE,
        senha TEXT NOT NULL
    )
''')

# Cria um usuário padrão (admin / 1234) caso não exista
cursor.execute("INSERT OR IGNORE INTO usuarios (usuario, senha) VALUES (?, ?)", ("admin", "1234"))

conexao.commit()
conexao.close()

print("Banco de dados e tabelas criados com sucesso!")
