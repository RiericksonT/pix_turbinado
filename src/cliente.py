import socket

DNS_HOST = '127.0.0.1'
DNS_PORT = 53

def get_load_balancer_address(domain):
    # Conecte-se ao servidor DNS e obtenha o endereço IP e a porta do balanceador de carga para o domínio especificado
    dns_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    dns_socket.connect((DNS_HOST, DNS_PORT))
    dns_socket.sendall(domain.encode())
    response = dns_socket.recv(1024).decode()
    dns_socket.close()
    return response.split(':')

def send_request_to_load_balancer(address, request):
    # Conecte-se ao balanceador de carga e envie a solicitação
    lb_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    lb_socket.connect((address[0], int(address[1])))
    lb_socket.sendall(request.encode())
    response = lb_socket.recv(1024).decode()
    lb_socket.close()
    return response

# Solicite o domínio ao usuário
domain = input("Digite o domínio: ")

# Obtenha o endereço do balanceador de carga para o domínio especificado
lb_address = get_load_balancer_address(domain)

# Envie uma solicitação para o balanceador de carga
request = "GET /"
response = send_request_to_load_balancer(lb_address, request)

# Processar a resposta
print("Resposta recebida:", response)