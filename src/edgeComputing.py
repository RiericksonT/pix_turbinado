##############
# Precisamos colocar um mutex aqui nesse codigo eu acho
##############

# Código do servidor de aplicação
import socket
import re
from time import sleep
import geradorMensagem

HOST = '127.0.0.1'
PORT = 5000
F = 25  # Tamanho fixo da mensagem em bytes

HOST_DADOS = '127.0.0.1'
PORT_DADOS = 10001

# create a regex to validate the request, the format correct is "0|0|0|0000"
request_mold = re.compile(r'^[1-9]\|[0-9]{1,8}\|[0-9]{1,3}\|[0-9]{1,11}$')


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
    request = client_socket.recv(F).decode()
    
    # Processar a requisição e enviar a resposta, compare with request_mold

    if request_mold.match(request) and request.split('|')[0] == '1':
        #verify the logados array in the data service
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.connect((HOST_DADOS, PORT_DADOS))
        server_socket.sendall(request.encode())

        response = server_socket.recv(F).decode()
        if response.split('|')[1] == '1':
            client_socket.sendall(response.encode())

    elif request_mold.match(request) and request.split('|')[0] == '3':
        # editar isso para chamar a função certa no serviço de dados
        sleep(10)
        client_socket.sendall('Operation completed successfully'.encode())

    elif request_mold.match(request) and request.split('|')[0] == '4':
        # editar isso para chamar a função certa no serviço de dados
        client_socket.sendall('cliente saiu'.encode())

    elif request_mold.match(request) and request.split('|')[0] == '7':
        
        # editar isso para chamar a função certa no serviço de dados
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.connect((HOST_DADOS, PORT_DADOS))
        server_socket.sendall(request.encode())
        response = server_socket.recv(F).decode()
        
        if response.split('|')[1] == '1':
            client_socket.sendall(response.encode())
            
        else:
            client_socket.sendall('Login incorreto!'.encode())
            client_socket.close()
            

    else:
        response = "ERROR - Invalid request" + (f'{request}')
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
