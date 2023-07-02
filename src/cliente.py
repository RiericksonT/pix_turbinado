import socket
import time
import geradorMensagem
import random


DNS_HOST = '127.0.0.1'
DNS_PORT = 53

F = 2048  # Tamanho fixo da mensagem em bytes
op = 10



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
rand_acc = random.randint(0, 20)
# Obtenha o endereço do balanceador de carga para o domínio especificado
lb_address = get_load_balancer_address(domain)

response = send_request_to_load_balancer(lb_address, f'7|{rand_acc}|123|0|0')
print(response)
if response.split('|')[1] == "1":
    for i in range(0, op):
        a = random.randint(0, 20)
        rand_acc2 = a if rand_acc == a else rand_acc + 1 if rand_acc < 20 else rand_acc - 1
        rand_val = random.randint(0, 99999999)
        # Envie uma solicitação para o balanceador de carga
        request = geradorMensagem.gerador_msg(1, 0, 0, 0)
        print(f'my request: {request}')
        response = send_request_to_load_balancer(lb_address, request)
        print(f'Respostas depois de solicitar acesso {response}')

        if response.split('|')[1] == "1":
            operation = geradorMensagem.gerador_msg(
                3, rand_acc, rand_acc2, rand_val)
            print(f'operacao {operation}')
            response = send_request_to_load_balancer(lb_address, operation)
            print(f'resposta dps da operação {response}')
            time.sleep(5)
            exit_msg = geradorMensagem.gerador_msg(4, 0, 0, 0)
            response = send_request_to_load_balancer(lb_address, exit_msg)
            print(f'Saindo... {response}')
        else:
            print("Não foi acessar a conta, por favor espere...")
            continue
else:
    print("Não foi possível fazer login no servidor, por favor tente novamente mais tarde.")
