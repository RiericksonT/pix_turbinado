# Código do servidor de dados
import socket
import random
import sqlite3
import threading

conn = sqlite3.connect('./database/banco_de_dados.db')
cursor = conn.cursor()

HOST = '127.0.0.1'
PORT = 10001
F = 28  # Tamanho fixo da mensagem em bytes

quantity = 20

logados = []

queue = []
accessing_now = []

def write_file(text):
    with open('log_server.txt', 'a') as file:
        file.write(text)


def read_file(id):
    with open('log_server.txt', 'r') as file:
        # count how many times the server was accessed by the client
        count = 0
        for line in file:
            if line.split()[1] == id and line.split()[3] == 'access':
                count += 1
        return (f'Account {id} was accessed {count} times')

def terminal():
    global queue
    global accessing_now

    while True:
        command = input(
            "1 - Show queue | 2 - Show accessing now | 3 - Show accounts | 4 - Show quantity times process\n")
        if command == '1':
            print(queue)
        elif command == '2':
            print(accessing_now)
        elif command == '3':
            print(logados)
        elif command == '4':
            print(read_file(input('id: ')))
        else:
            print('Invalid command')
            continue

def generate_accounts(quantity):
    accounts = []
    sql_verify = "SELECT * FROM contas"
    cursor.execute(sql_verify)
    accounts = cursor.fetchall()
    if len(accounts) > 0:
        write_file('Accounts already generated\n')
    else:
        for i in range(quantity):
            sql = "INSERT INTO contas (dono, senha, saldo) VALUES (?, ?, ?)"
            dados_cliente = (i, '123', random.randint(0, 99999999))
            cursor.execute(sql, dados_cliente)

            conn.commit()
        conn.close()


def login(message, edge_socket):
    conn = sqlite3.connect('./database/banco_de_dados.db')
    cursor = conn.cursor()

    dono = message.split('|')[1]
    password = message.split('|')[2]

    sql = "SELECT * FROM contas WHERE dono = ? AND senha = ?"
    dados_cliente = (dono, password)
    cursor.execute(sql, dados_cliente)
    result = cursor.fetchall()
    if len(result) > 0:
        edge_socket.sendall('7|1|0'.encode())
        logados.append(dono)
        write_file(f'{dono} with {password} access account\n')
    else:
        edge_socket.sendall('7|0|0|0'.encode())

        edge_socket.close()


def handle_client_request(client_socket):
    # Lógica para armazenar e recuperar os dados relevantes
    request = client_socket.recv(2048).decode()
    print(request)
    msg_id = request.split('|')[0]
    conta_origem = request.split('|')[2]
    conta_destino = request.split('|')[3]
    valor = request.split('|')[4]

    if msg_id == '3':
        sql = "SELECT saldo FROM contas WHERE dono = ?"
        dados_cliente = (conta_origem)
        cursor.execute(sql, dados_cliente)
        result = cursor.fetchall()
        if result[0][0] >= int(valor):
            sql = "UPDATE contas SET saldo = saldo - ? WHERE dono = ?"
            dados_cliente = (valor, conta_origem)
            cursor.execute(sql, dados_cliente)
            conn.commit()

            sql = "UPDATE contas SET saldo = saldo + ? WHERE dono = ?"
            dados_cliente = (valor, conta_destino)
            cursor.execute(sql, dados_cliente)
            conn.commit()

            write_file(f'{conta_origem} transfered {valor} to {conta_destino}\n')
            write_file(f'{conta_destino} received {valor} from {conta_origem}\n')
            client_socket.sendall('4|1|0|0'.encode())
        else:
            client_socket.sendall('8|0|0|0'.encode())


# Inicie o servidor de dados
data_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
data_server.bind((HOST, PORT))
data_server.listen()

threading.Thread(target=terminal).start()
generate_accounts(quantity)

while True:
    edge_socket, _ = data_server.accept()
    message = edge_socket.recv(F).decode()
    if message.split('|')[0] == '7':
        threading.Thread(target=login, args=(message, edge_socket)).start()
    elif message.split('|')[0] == '1' and message.split('|')[1] in logados:
        threading.Thread(target=handle_client_request, args=(edge_socket,)).start()
    else:
        edge_socket.sendall('1|1|0'.encode())
        edge_socket.close()
        
