import socket
import re
from time import sleep
import geradorMensagem
import threading  # Importar o módulo threading para usar mutex

HOST = '127.0.0.1'
PORT = 5000
F = 2048  # Tamanho fixo da mensagem em bytes

HOST_DADOS = '127.0.0.1'
PORT_DADOS = 10001

request_mold = re.compile(r'^[1-9]\|[0-9]{1,8}\|[0-9]{1,3}\|[0-9]{1,8}\|[0-9]{1,11}$')

mutex = threading.Lock()  # Inicializar o mutex


def is_port_in_use(port):
    try:
        test_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        test_socket.bind(('127.0.0.1', port))
        test_socket.close()
        return False
    except OSError:
        return True


def handle_client_request(client_socket):
    request = client_socket.recv(F).decode()

    if request_mold.match(request) and request.split('|')[0] == '1':
        mutex.acquire()  # Adquirir o mutex antes de acessar o servidor de dados

        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.connect((HOST_DADOS, PORT_DADOS))
        server_socket.sendall(request.encode())

        response = server_socket.recv(2048).decode()
        print(f'edge compute: {response}')
        if response.split('|')[1] == '1':
            client_socket.sendall(response.encode())

        server_socket.close()

        mutex.release()  # Liberar o mutex após acessar o servidor de dados

    elif request_mold.match(request) and request.split('|')[0] == '3':
        mutex.acquire()  # Adquirir o mutex antes de acessar o servidor de dados

        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.connect((HOST_DADOS, PORT_DADOS))
        print(f'edge compute 2: {request}')
        server_socket.sendall(request.encode())
        response = server_socket.recv(F).decode()
        print(f'edge compute 3: {response}')
        if response.split('|')[1] == '1':
            client_socket.sendall(response.encode())
        else:
            client_socket.sendall('Saldo insuficiente!'.encode())
            client_socket.close()

        server_socket.close()

        mutex.release()  # Liberar o mutex após acessar o servidor de dados

    elif request_mold.match(request) and request.split('|')[0] == '4':
        mutex.acquire()  # Adquirir o mutex antes de acessar o servidor de dados

        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.connect((HOST_DADOS, PORT_DADOS))
        server_socket.sendall(request.encode())
        client_socket.sendall('cliente saiu'.encode())

        server_socket.close()

        mutex.release()  # Liberar o mutex após acessar o servidor de dados

    elif request_mold.match(request) and request.split('|')[0] == '7':
        mutex.acquire()  # Adquirir o mutex antes de acessar o servidor de dados

        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.connect((HOST_DADOS, PORT_DADOS))
        server_socket.sendall(request.encode())
        response = server_socket.recv(F).decode()

        if response.split('|')[1] == '1':
            client_socket.sendall(response.encode())
        else:
            client_socket.sendall('Login incorreto!'.encode())
            client_socket.close()

        server_socket.close()

        mutex.release()  # Liberar o mutex após acessar o servidor de dados

    else:
        response = "ERROR - Invalid request" + (f'{request}')
        client_socket.sendall(response.encode())
        client_socket.close()


# Iniciar o servidor de aplicação
if is_port_in_use(PORT):
    PORT += 1
    application_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    application_server.bind((HOST, PORT))
    application_server.listen()
else:
    application_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    application_server.bind((HOST, PORT))
    application_server.listen()

print(f'Servidor iniciado em {HOST}:{PORT}')

while True:
    client_socket, _ = application_server.accept()
    threading.Thread(target=handle_client_request, args=(client_socket,)).start()
