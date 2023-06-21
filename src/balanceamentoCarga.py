import socket

# Lista de endereços de sockets
socket_addresses = [
    ('localhost', 5000),
    ('localhost', 5001)
]

# Fila de sockets
socket_queue = list(socket_addresses)


def load_balancer(request):
    # Obtém o próximo socket da fila
    socket_address = socket_queue.pop(0)

    # Envia a requisição para o socket selecionado
    response = send_request(socket_address, request)

    # Adiciona o socket usado de volta à fila
    socket_queue.append(socket_address)

    return response


def send_request(socket_address, request):
    # Cria um socket TCP
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        # Conecta ao socket selecionado
        sock.connect(socket_address)

        # Envia a requisição
        sock.sendall(request.encode())

        # Recebe a resposta
        response = sock.recv(1024).decode()

        return response
    finally:
        # Fecha o socket
        sock.close()


# Exemplo de uso
while True:
    request = input('Digite uma mensagem: ')
    response = load_balancer(request)
    print(response)
