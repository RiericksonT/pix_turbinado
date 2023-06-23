import socket
import geradorMensagem
import random


DNS_HOST = '127.0.0.1'
DNS_PORT = 53

F = 25  # Tamanho fixo da mensagem em bytes
op = 10
rand_acc = random.randint(0, 99)
rand_val = random.randint(0, 99999999)


def get_load_balancer_address(domain):
    # Conecte-se ao servidor DNS e obtenha o endereço IP e a porta do balanceador de carga para o domínio especificado
    dns_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    dns_socket.connect((DNS_HOST, DNS_PORT))
    dns_socket.sendall(domain.encode())
    response = dns_socket.recv(F).decode()
    dns_socket.close()
    return response.split(':')


def send_request_to_load_balancer(address, request):
    # Conecte-se ao balanceador de carga e envie a solicitação
    lb_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    lb_socket.connect((address[0], int(address[1])))
    lb_socket.sendall(request.encode())
    response = lb_socket.recv(F).decode()
    lb_socket.close()
    return response


# Solicite o domínio ao usuário
domain = input("Digite o domínio: ")

# Obtenha o endereço do balanceador de carga para o domínio especificado
lb_address = get_load_balancer_address(domain)

response = send_request_to_load_balancer(lb_address, '7|2|123|0')
if response.split('|')[1] == "1":
    for i in range(0, op):
        # Envie uma solicitação para o balanceador de carga
        request = geradorMensagem.gerador_msg(1, 0, 0)
        response = send_request_to_load_balancer(lb_address, request)
        print(request)

        if response.split('|')[0] == "2":
            operation = geradorMensagem.gerador_msg(3, rand_acc, rand_val)
            response = send_request_to_load_balancer(lb_address, operation)
            print(response)
            exit_msg = geradorMensagem.gerador_msg(4, 0, 0)
            response = send_request_to_load_balancer(lb_address, exit_msg)
            print('saindo...')
        else:
            print("Não foi acessar a conta, por favor espere...")
            continue
else:
    print("Não foi possível fazer login no servidor, por favor tente novamente mais tarde.")
