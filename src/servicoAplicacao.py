# Código do servidor de aplicação
import socket

HOST = '127.0.0.1'
PORT = 9001

def handle_client_request(client_socket):
    # Lógica para processar as operações transacionais e acessar o servidor de dados
    request = client_socket.recv(1024).decode().strip()

    # Processar a requisição e enviar a resposta
    response = process_request(request)
    client_socket.sendall(response.encode())
    client_socket.close()

# Inicie o servidor de aplicação
application_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
application_server.bind((HOST, PORT))
application_server.listen()

while True:
    client_socket, _ = application_server.accept()
    handle_client_request(client_socket)