import socket

HOST = '127.0.0.1'
PORT = 7000
F = 25  # Tamanho fixo da mensagem em bytes

# Lista de endereços de sockets
socket_addresses = [
    ('localhost', 5000),
    ('localhost', 5001)
]

# Fila de sockets
socket_queue = list(socket_addresses)


def load_balancer(request, socket_requesting):
    # Obtém o próximo socket da fila
    socket_address = socket_queue.pop(0)

    # Envia a requisição para o socket selecionado
    response = send_request(socket_address, request, socket_requesting)

    # Adiciona o socket usado de volta à fila
    socket_queue.append(socket_address)

    return response


def send_request(socket_address, request, socket_requesting):
    # Cria um socket TCP
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        # Conecta ao socket selecionado
        sock.connect(socket_address)

        # Envia a requisição
        sock.sendall(request.encode())

        # Recebe a resposta
        response = sock.recv(F).decode()

        # Envia a resposta para o socket que solicitou
        socket_requesting.sendall(response.encode())

        return response
    finally:
        # Fecha o socket
        sock.close()


loadbalancer_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
loadbalancer_server.bind((HOST, PORT))
loadbalancer_server.listen()
# Exemplo de uso
while True:
    # listen new connection
    client_socket, _ = loadbalancer_server.accept()
    request = client_socket.recv(F).decode()
    load_balancer(request, client_socket)
