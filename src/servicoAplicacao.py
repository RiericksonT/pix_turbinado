# Código do servidor de dados
import socket

HOST = '127.0.0.1'
PORT = 10001
F = 25  # Tamanho fixo da mensagem em bytes


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

while True:
    client_socket, _ = data_server.accept()
    handle_client_request(client_socket)
