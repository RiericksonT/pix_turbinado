import subprocess
import threading


def run_dns():
    dns = "python ./src/dns.py"
    subprocess.run(dns, shell=True)


def run_balanceamentoCarga():
    balanceamentoCarga = "python ./src/balanceamentoCarga.py"
    subprocess.run(balanceamentoCarga, shell=True)


def run_servicoAplicacao():
    servicoAplicacao = "python ./src/servicoAplicacao.py"
    subprocess.run(servicoAplicacao, shell=True)


def run_servicoDados():
    servicoDados = "python ./src/servicoDados.py"
    subprocess.run(servicoDados, shell=True)


server_thread = threading.Thread(target=run_dns)
server_thread.start()
server_thread = threading.Thread(target=run_balanceamentoCarga)
server_thread.start()
server_thread = threading.Thread(target=run_servicoAplicacao)
server_thread.start()
server_thread = threading.Thread(target=run_servicoDados)
server_thread.start()
