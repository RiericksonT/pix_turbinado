import datetime
import random
import socket
import threading
import time
import sqlite3

conn = sqlite3.connect('./database/banco_de_dados.db')
cursor = conn.cursor()


queue = []
contas = []
fila_lock = threading.Lock()
accessing_now = None
m = 10

time_start = time.time()

nameP = 'cliente'
passwordP = '123'

HOST = 'localhost'
PORT = 10001
BUFFER = 1024

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen()


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


def gen_account(quantity):
    for i in range(quantity):
        sql = "INSERT INTO clientes (nome, email, saldo) VALUES (?, ?, ?)"
        dados_cliente = (i, f'{i}@example.com', random.randint(0, 99999999))
        cursor.execute(sql, dados_cliente)

        conn.commit()
        conn.close()


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
        return count


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
            print(contas)
        elif command == '4':
            print(read_file(input('id: ')))
        else:
            print('Invalid command')
            continue


def login(conn, addr):
    name = conn.recv(BUFFER).decode('utf-8')
    print(f'login: {name}')
    password = conn.recv(BUFFER).decode('utf-8')
    print(f'password: {password}')

    if name == nameP and password == passwordP:
        thread_handle = threading.Thread(
            target=handle_cliente, args=(conn, addr))
        thread_handle.start()
    else:
        print('login error')
        conn.send(f'5|0101|000'.encode('utf-8'))


def handle_cliente(conn, addr):
    global accessing_now
    global time_start

    while True:
        try:
            msg = conn.recv(BUFFER).decode()

            if time.time() - time_start < 300:
                if msg.split('|')[0] == "1":
                    queue.append(conn)
                    write_file(
                        f"Client {msg.split('|')[1]} solicitou acesso ao servidor\n")

                    while accessing_now != conn:
                        continue

                    if conn:
                        write_file(
                            f"Client {msg.split('|')[1]} has access to make op at {datetime.datetime.now()}\n")
                        conn.send(f'2|0101|00'.encode('utf-8'))
                        time_start = time.time()

                elif msg.split('|')[0] == "3":
                    for acc in contas:
                        if int(msg.split('|')[1]) == acc['id']:
                            if acc['saldo'] < int(msg.split('|')[3]):
                                acc['saldo'] -= int(msg.split('|')[3])
                                write_file(
                                    f"Client {msg.split('|')[1]} make a op to {msg.split('|')[2]} - Value {msg.split('|')[3]}\n"
                                )

                                for acc1 in contas:
                                    if int(msg.split('|')[2]) == acc1['id']:
                                        acc1['saldo'] += int(msg.split('|')[3])
                                        write_file(
                                            f"Client {msg.split('|')[2]} recive a op to {msg.split('|')[1]} - Value {msg.split('|')[3]}\n"
                                        )
                            else:
                                conn.send(f'7|0101|00'.encode('utf-8'))

                elif msg.split('|')[0] == "4":
                    write_file(
                        f"Client {msg.split('|')[1]} has left the critical region at {datetime.datetime.now()}\n")
                    accessing_now = None
            else:
                conn.send(f'4|0101|00'.encode('utf-8'))
                accessing_now = None
                time_start = time.time()

        except ConnectionError:
            continue


threading.Thread(target=terminal).start()
threading.Thread(target=exc_mut).start()
gen_account(m)

while True:
    conn, addr = server.accept()
    threading.Thread(target=login, args=(conn, addr)).start()
