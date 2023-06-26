# Código do servidor de dados
import datetime
import socket
import random
import sqlite3
import threading

conn = sqlite3.connect('./database/banco_de_dados.db')
cursor = conn.cursor()

HOST = '127.0.0.1'
PORT = 10001
F = 2048  # Tamanho fixo da mensagem em bytes

# Inicie o servidor de dados
data_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
data_server.bind((HOST, PORT))
data_server.listen()

quantity = 20

logados = []

queue = []
accessing_now = None

lock = threading.Lock()

class Semaphore:
    def __init__(self, value):
        self.value = value
        self.queue = []

    def acquire(self):
        self.queue.append(threading.current_thread())
        while self.queue[0] != threading.current_thread() or self.value == 0:
            pass
        self.value -= 1
        self.queue.pop(0)

    def release(self):
        self.value += 1


semaphore = Semaphore(1)

def write_file(text):
    with open('log_server.txt', 'a') as file:
        file.write(text)


def read_file(id):
    with open('log_server.txt', 'r') as file:
        # count how many times the server was accessed by the client
        count = 0
        for line in file:
            if line.split()[0] == id:
                count += 1
        return (f'Account {id} was accessed {count} times')
    
def exc_mut():
    global accessing_now
    while True:
        if len(queue) > 0:
            if accessing_now is None:
                semaphore.acquire()
                accessing_now = queue.pop(0)
                semaphore.release()

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
        edge_socket.sendall('7|1|0|0'.encode())
        logados.append(dono)
        write_file(f'{dono} with {password} access account\n')
    else:
        edge_socket.sendall('7|0|0|0'.encode())

        edge_socket.close()

def send_pix(client_socket, message):
    conn = sqlite3.connect('./database/banco_de_dados.db')
    cursor = conn.cursor()
    
    print(f'PIX request: {message}')
    msg_id = message.split('|')[0]
    conta_origem = message.split('|')[2].zfill(2)
    conta_destino = message.split('|')[3]
    valor = message.split('|')[4]

    if msg_id == '3':
        sql = "SELECT saldo FROM contas WHERE dono = ?"
        dados_cliente = (conta_origem,)
        cursor.execute(sql, dados_cliente)
        result = cursor.fetchall()
        print(result)
        if result.__len__() > 0 and result[0][0] >= int(valor):
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
            write_file(f'{conta_origem} failed to transfer {valor} to {conta_destino}\n')
            client_socket.sendall('8|0|0|0'.encode())

def handle_client_request(message, edge_socket):

    global queue
    global accessing_now
    # Lógica para armazenar e recuperar os dados relevantes
    print(f'Handling client request: {message}')
    if message.split('|')[0] == '1':
        queue.append(edge_socket)
        print(f'Queue: {queue} and accessing now: {accessing_now}')
        print(f'Client {message.split("|")[1]} has been added to the queue')
        write_file(
            f"Client {message.split('|')[1]} solicitou acesso ao servidor\n")

        while accessing_now != edge_socket:
            continue

        if edge_socket:
            write_file(
                f"Client {message.split('|')[1]} has access to make op at {datetime.datetime.now()}\n")
            edge_socket.send(f'2|1|00'.encode('utf-8'))
            edge_socket.close()
    elif message.split('|')[0] == '3':
        print(f'PIX: {message}')
        send_pix(edge_socket, message)

    elif message.split('|')[0] == "4":
        write_file(
            f"Client {message.split('|')[1]} has left the critical region at {datetime.datetime.now()}\n")
        accessing_now = None

    elif message.split('|')[0] == '7':
        login(message, edge_socket)

threading.Thread(target=exc_mut).start()
threading.Thread(target=terminal).start()
generate_accounts(quantity)

while True:
    edge_socket, _ = data_server.accept()
    message = edge_socket.recv(F).decode()
    threading.Thread(target=handle_client_request, args=(message, edge_socket)).start()

        
