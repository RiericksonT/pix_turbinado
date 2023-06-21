# Código do servidor de aplicação
import socket

HOST = '127.0.0.1'
PORT = 5000


def is_port_in_use(port):
    try:
        test_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        test_socket.bind(('127.0.0.1', port))
        test_socket.close()
        return False
    except OSError:
        return True


def handle_client_request(client_socket):
    # Lógica para processar as operações transacionais e acessar o servidor de dados
    request = client_socket.recv(1024).decode().strip()

    # Processar a requisição e enviar a resposta
    response = "OK " + (f'{PORT}')
    client_socket.sendall(response.encode())
    client_socket.close()


# Inicie o servidor de aplicação
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
    handle_client_request(client_socket)
