import multiprocessing
import subprocess

def run_dns():
    dns = "python ./src/dns.py"
    subprocess.run(dns, shell=True)

def run_balanceamentoCarga():
    balanceamentoCarga = "python ./src/balanceamentoCarga.py"
    subprocess.run(balanceamentoCarga, shell=True)

def run_edgeComputing():
    edgeComputing = "python ./src/edgeComputing.py"
    subprocess.run(edgeComputing, shell=True)

def run_servicoAplicacao():
    servicoAplicacao = "python ./src/servicoAplicacao.py"
    subprocess.run(servicoAplicacao, shell=True)

def run_cliente():
    cliente = "python ./src/cliente.py"
    subprocess.run(cliente, shell=True)

if __name__ == '__main__':
    process_dns = multiprocessing.Process(target=run_dns)
    process_dns.start()

    process_balanceamentoCarga = multiprocessing.Process(target=run_balanceamentoCarga)
    process_balanceamentoCarga.start()

    process_edgeComputing = multiprocessing.Process(target=run_edgeComputing)
    process_edgeComputing.start()

    process_edgeComputing2 = multiprocessing.Process(target=run_edgeComputing)
    process_edgeComputing2.start()

    process_servicoAplicacao = multiprocessing.Process(target=run_servicoAplicacao)
    process_servicoAplicacao.start()

    process_cliente = multiprocessing.Process(target=run_cliente)
    process_cliente.start()
