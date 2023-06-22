import os

F = 25  # Tamanho fixo da mensagem em bytes
SEPARATOR = '|'  # Separador dos campos da mensagem


def gerador_msg(msg_id, conta_destino, valor):
    # Identificador da mensagem (0 a 9)
    msg_id = str(msg_id).zfill(1)
    # Identificador do processo (0 a 99999999)
    process_id = str(os.getpid()).zfill(8)
    # Identificador da conta de destino (0 a 99)
    conta_destino = str(conta_destino).zfill(2)
    valor = str(valor).zfill(11)  # Valor da transferência (0 a 99999999999)
    return (msg_id + SEPARATOR + process_id + SEPARATOR + conta_destino + SEPARATOR + valor).zfill(F)


msg = gerador_msg(1, 0, 0)
print(msg, len(msg))
