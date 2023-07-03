import unittest
import socket
from threading import Thread


class DNSTestCase(unittest.TestCase):
    def setUp(self):
        # Configuração do servidor DNS
        self.HOST = '127.0.0.1'
        self.PORT = 53
        self.F = 28

        self.dns_table = {
            'www.example.com': ('127.0.0.1', 7000)
        }

        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((self.HOST, self.PORT))
        self.server_socket.listen()

        # Iniciar o servidor DNS em uma thread separada
        self.server_thread = Thread(target=self.start_dns_server)
        self.server_thread.start()

    def tearDown(self):
        # Encerrar o servidor DNS e aguardar a conclusão da thread
        self.server_socket.close()
        self.server_thread.join()

    def start_dns_server(self):
        while True:
            client_socket, _ = self.server_socket.accept()
            self.handle_dns_request(client_socket)

    def handle_dns_request(self, client_socket):
        data = client_socket.recv(self.F)
        domain = data.decode().strip()

        if domain in self.dns_table:
            ip, port = self.dns_table[domain]
            response = f"{ip}:{port}"
        else:
            response = "Domain not found"

        client_socket.sendall(response.encode())
        client_socket.close()

    def test_existing_domain(self):
        # Conectar ao servidor DNS e enviar uma solicitação para um domínio existente
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((self.HOST, self.PORT))
        client_socket.sendall('www.example.com'.encode())

        # Receber a resposta do servidor DNS
        response = client_socket.recv(self.F).decode()

        # Verificar se a resposta está correta
        self.assertEqual(response, '127.0.0.1:7000')

        # Fechar o socket do cliente
        client_socket.close()

    def test_nonexistent_domain(self):
        # Conectar ao servidor DNS e enviar uma solicitação para um domínio inexistente
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((self.HOST, self.PORT))
        client_socket.sendall('nonexistent.com'.encode())

        # Receber a resposta do servidor DNS
        response = client_socket.recv(self.F).decode()

        # Verificar se a resposta está correta
        self.assertEqual(response, 'Domain not found')

        # Fechar o socket do cliente
        client_socket.close()


if __name__ == '__main__':
    unittest.main()


# import unittest
# import threading
# import socket

# # Definir as informações do servidor de teste
# TEST_HOST = '127.0.0.1'
# TEST_PORT = 8000

# # Definir a mensagem de teste
# TEST_DOMAIN = 'www.example.com'

# class TestDNSServer(unittest.TestCase):

#     @classmethod
#     def setUpClass(cls):
#         # Iniciar o servidor DNS em uma thread separada
#         server_thread = threading.Thread(target=run_dns_server)
#         server_thread.daemon = True
#         server_thread.start()

#     def test_handle_dns_request(self):
#         # Criar um socket cliente para se conectar ao servidor DNS
#         client_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#         client_sock.connect((TEST_HOST, TEST_PORT))

#         # Enviar uma solicitação de teste
#         client_sock.sendall(TEST_DOMAIN.encode())

#         # Receber a resposta do servidor DNS
#         response = client_sock.recv(1024).decode()

#         # Verificar se a resposta está correta
#         self.assertEqual(response, '127.0.0.1:7000')

#         # Fechar o socket cliente
#         client_sock.close()

# def run_dns_server():
#     dns_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#     dns_server.bind((TEST_HOST, TEST_PORT))
#     dns_server.listen()

#     while True:
#         client_socket, _ = dns_server.accept()
#         handle_dns_request(client_socket)

# if __name__ == '__main__':
#     unittest.main()
