# Código do servidor DNS
import socket

HOST = '127.0.0.1'
PORT = 53

dns_table = {
    # Exemplo de mapeamento de domínio para endereço IP e porta do balanceador de carga
    'www.example.com': ('127.0.0.1', 7000)
}


def handle_dns_request(client_socket):
    data = client_socket.recv(1024)
    domain = data.decode().strip()

    if domain in dns_table:
        ip, port = dns_table[domain]
        response = f"{ip}:{port}"
    else:
        response = "Domain not found"

    client_socket.sendall(response.encode())
    client_socket.close()


# Inicie o servidor DNS
dns_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
dns_server.bind((HOST, PORT))
dns_server.listen()

while True:
    client_socket, _ = dns_server.accept()
    handle_dns_request(client_socket)
