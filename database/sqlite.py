import sqlite3

# Conectar ao banco de dados (irá criar um novo banco de dados se não existir)
conn = sqlite3.connect('./database/banco_de_dados.db')

# Criar um cursor para executar comandos SQL
cursor = conn.cursor()

# Criar tabela "contas"
cursor.execute('''CREATE TABLE IF NOT EXISTS contas
                  (id INTEGER PRIMARY KEY AUTOINCREMENT,
                   dono TEXT NOT NULL,
                   senha TEXT NOT NULL,
                   saldo REAL)''')

# Criar tabela "historico_transacoes"
cursor.execute('''CREATE TABLE IF NOT EXISTS historico_transacoes
                  (id INTEGER PRIMARY KEY AUTOINCREMENT,
                   conta_origem_id INTEGER,
                   conta_destino_id INTEGER,
                   data_transacao TEXT,
                   valor REAL,
                   FOREIGN KEY (conta_origem_id) REFERENCES contas (id),
                   FOREIGN KEY (conta_destino_id) REFERENCES contas (id))''')

# Commit (confirmar) as alterações no banco de dados
conn.commit()

# Fechar a conexão com o banco de dados
conn.close()
