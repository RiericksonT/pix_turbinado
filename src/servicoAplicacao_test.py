import unittest
import threading
import socket
import sqlite3

from edgeComputing import handle_client_request

# Definir as informações do servidor de teste
TEST_HOST = '127.0.0.1'
TEST_PORT = 8000

# Definir as informações do servidor de dados
DATA_HOST = '127.0.0.1'
DATA_PORT = 10001

# Definir a mensagem de teste
TEST_MESSAGE = '1|100|1|100|1000'


class TestDataServer(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Iniciar o servidor de dados em uma thread separada
        server_thread = threading.Thread(target=run_data_server)
        server_thread.daemon = True
        server_thread.start()

    def test_handle_client_request(self):
        # Criar um socket cliente para se conectar ao servidor de dados
        client_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_sock.connect((DATA_HOST, DATA_PORT))

        # Enviar uma solicitação de teste
        client_sock.sendall(TEST_MESSAGE.encode())

        # Receber a resposta do servidor de dados
        response = client_sock.recv(1024).decode()

        # Verificar se a resposta está correta
        self.assertEqual(response, 'response_test')

        # Fechar o socket cliente
        client_sock.close()


def run_data_server():
    conn = sqlite3.connect('./database/banco_de_dados.db')
    cursor = conn.cursor()

    data_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    data_server.bind((TEST_HOST, TEST_PORT))
    data_server.listen()

    while True:
        client_socket, _ = data_server.accept()
        handle_client_request(client_socket)


if __name__ == '__main__':
    unittest.main()
