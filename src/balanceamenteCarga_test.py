import unittest
import threading
import socket
import time
from queue import Queue

# Definir as informações do servidor de teste
TEST_HOST = '127.0.0.1'
TEST_PORT = 8000

# Definir informações do servidor de balanceamento de carga
LOAD_BALANCER_HOST = '127.0.0.1'
LOAD_BALANCER_PORT = 7000

# Definir informações dos servidores de back-end
SERVER_1_HOST = '127.0.0.1'
SERVER_1_PORT = 5000

SERVER_2_HOST = '127.0.0.1'
SERVER_2_PORT = 5001

# Definir a mensagem de teste
TEST_MESSAGE = 'Test message'

# Fila de mensagens recebidas pelos servidores de back-end
message_queue = Queue()


def server_1():
    server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_sock.bind((SERVER_1_HOST, SERVER_1_PORT))
    server_sock.listen()

    while True:
        client_socket, _ = server_sock.accept()
        request = client_socket.recv(1024).decode()
        message_queue.put((SERVER_1_HOST, SERVER_1_PORT, request))
        response = 'Response from server 1'
        client_socket.sendall(response.encode())
        client_socket.close()


def server_2():
    server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_sock.bind((SERVER_2_HOST, SERVER_2_PORT))
    server_sock.listen()

    while True:
        client_socket, _ = server_sock.accept()
        request = client_socket.recv(1024).decode()
        message_queue.put((SERVER_2_HOST, SERVER_2_PORT, request))
        response = 'Response from server 2'
        client_socket.sendall(response.encode())
        client_socket.close()


class TestLoadBalancer(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Iniciar os servidores de back-end em threads separadas
        server1_thread = threading.Thread(target=server_1)
        server2_thread = threading.Thread(target=server_2)
        server1_thread.daemon = True
        server2_thread.daemon = True
        server1_thread.start()
        server2_thread.start()

        # Aguardar um curto período para os servidores iniciarem
        time.sleep(0.1)

    def test_load_balancer(self):
        # Criar um socket cliente para se conectar ao servidor de balanceamento de carga
        client_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_sock.connect((LOAD_BALANCER_HOST, LOAD_BALANCER_PORT))

        # Enviar uma solicitação de teste
        client_sock.sendall(TEST_MESSAGE.encode())

        # Receber a resposta do servidor de balanceamento de carga
        response = client_sock.recv(1024).decode()

        # Verificar se a resposta veio de um dos servidores de back-end
        self.assertIn(
            response, ['Response from server 1', 'Response from server 2'])

        # Obter as informações do servidor de back-end da fila de mensagens
        server_host, server_port, request = message_queue.get()

        # Verificar se a mensagem recebida pelos servidores de back-end é a mesma que a enviada pelo cliente
        self.assertEqual(request, TEST_MESSAGE)

        # Verificar se o servidor de balanceamento de carga encaminhou a solicitação para o servidor de back-end correto
        if response == 'Response from server 1':
            self.assertEqual((server_host, server_port),
                             (SERVER_1_HOST, SERVER_1_PORT))
        else:
            self.assertEqual((server_host, server_port),
                             (SERVER_2_HOST, SERVER_2_PORT))

        # Fechar o socket cliente
        client_sock.close()


if __name__ == '__main__':
    unittest.main()
