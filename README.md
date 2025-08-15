# Sistema Padaria 🍞

Aplicação web simples para **gestão de produtos e usuários** de uma padaria, feita em **Flask + SQLite**.

> Projeto de portfólio — autenticação, CRUD de produtos, busca/ordenação, templates Jinja, sessões e filtros por categoria.


- Login/Logout (sessão via Flask)
- Listagem de produtos com **busca**, **filtro por categoria** e **ordenação**
- **CRUD**: cadastrar, editar e excluir produtos
- Templates com **Jinja2** e estilos CSS próprios
- Persistência com **SQLite** (arquivo local `padaria.db`)


- Python 3.10+
- Flask
- Jinja2
- Werkzeug

> O SQLite é embutido no Python; não precisa instalar servidor.


```bash
# 1) Clonar o repositório
git clone https://github.com/JoaoGabriel2003/sistema-padaria.git
cd sistema-padaria

# 2) (Opcional) criar virtualenv
python -m venv .venv
# Windows
.venv\Scripts\activate
# Linux/Mac
source .venv/bin/activate

# 3) Instalar dependências
pip install -r requirements.txt

# 4) Executar
python app.py
# Acesse http://127.0.0.1:5000
