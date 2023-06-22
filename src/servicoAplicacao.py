# Código do servidor de aplicação
import socket
import re

HOST = '127.0.0.1'
PORT = 5000

HOST_DADOS = '127.0.0.1'
PORT_DADOS = 6000

# create a regex to validate the request, the format correct is "0|0|0|0000"
request_mold = re.compile(r'^[1-4]\|[0-9]{2}\|[0-9]{2}\|[0-9]{8}$')


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

    # Processar a requisição e enviar a resposta, compare with request_mold

    if request_mold.match(request):
        print("Requisição recebida:", request)

    else:
        response = "ERROR - Invalid request"
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
