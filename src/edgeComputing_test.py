import unittest
import threading
import socket

from edgeComputing import handle_client_request

# Definir as informações do servidor de teste
TEST_HOST = '127.0.0.1'
TEST_PORT = 8000

# Definir informações do servidor de aplicação
APPLICATION_HOST = '127.0.0.1'
APPLICATION_PORT = 5000

# Definir a mensagem de teste
TEST_MESSAGE = '1|100|1|100|1000'


class TestApplicationServer(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Iniciar o servidor de aplicação em uma thread separada
        server_thread = threading.Thread(target=run_application_server)
        server_thread.daemon = True
        server_thread.start()

    def test_handle_client_request(self):
        # Criar um socket cliente para se conectar ao servidor de aplicação
        client_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_sock.connect((APPLICATION_HOST, APPLICATION_PORT))

        # Enviar uma solicitação de teste
        client_sock.sendall(TEST_MESSAGE.encode())

        # Receber a resposta do servidor de aplicação
        response = client_sock.recv(2048).decode()

        # Verificar se a resposta está correta
        self.assertEqual(response, 'response_test')

        # Fechar o socket cliente
        client_sock.close()


def run_application_server():
    application_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    application_server.bind((TEST_HOST, TEST_PORT))
    application_server.listen()

    while True:
        client_socket, _ = application_server.accept()
        handle_client_request(client_socket)


if __name__ == '__main__':
    unittest.main()
