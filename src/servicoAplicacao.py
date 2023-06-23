# Código do servidor de dados
import socket
import random
import sqlite3
import threading

conn = sqlite3.connect('./database/banco_de_dados.db')
cursor = conn.cursor()

HOST = '127.0.0.1'
PORT = 10001
F = 25  # Tamanho fixo da mensagem em bytes

quantity = 20

def generate_accounts(quantity):
    accounts = []
    sql_verify = "SELECT * FROM contas"
    cursor.execute(sql_verify)
    accounts = cursor.fetchall()
    if len(accounts) > 0:
        print('Banco de dados já populado')
    else:
        for i in range(quantity):
            sql = "INSERT INTO contas (dono, senha, saldo) VALUES (?, ?, ?)"
            dados_cliente = (i, '123', random.randint(0, 99999999))
            cursor.execute(sql, dados_cliente)

            conn.commit()
        print('Banco de dados populado com sucesso')
        conn.close()

def login(message, edge_socket):
    conn = sqlite3.connect('./database/banco_de_dados.db')
    cursor = conn.cursor()
    print(f'login attempt - {message}')

    dono = message.split('|')[1]
    password = message.split('|')[2]

    sql = "SELECT * FROM contas WHERE dono = ? AND senha = ?"
    dados_cliente = (dono, password)
    cursor.execute(sql, dados_cliente)
    result = cursor.fetchall()
    if len(result) > 0:
        edge_socket.sendall('7|1|0'.encode())
        print(f'login success - {message}')
        handle_client_request(edge_socket)
    else:
        edge_socket.sendall('7|0|0'.encode())
        print(f'login failed - {message}')
        edge_socket.close()

def handle_client_request(client_socket):
    # Lógica para armazenar e recuperar os dados relevantes
    request = client_socket.recv(F).decode().strip()

    # Acessar o banco de dados e processar a requisição
    response = process_database_request(request)
    client_socket.sendall(response.encode())
    client_socket.close()


# Inicie o servidor de dados
data_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
data_server.bind((HOST, PORT))
data_server.listen()

generate_accounts(quantity)

while True:
    edge_socket, _ = data_server.accept()
    message = edge_socket.recv(2048).decode()
    print(f'Data server recive - {message}')
    threading.Thread(target=login, args=(message, edge_socket)).start()
