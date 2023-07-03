import os

F = 28  # Tamanho fixo da mensagem em bytes
SEPARATOR = '|'  # Separador dos campos da mensagem


def gerador_msg(msg_id, process_id,conta_origem, conta_destino, valor):
    # Identificador da mensagem (0 a 9)
    msg_id = str(msg_id).zfill(1)
    # Identificador do processo (0 a 99999999)
    
    # Identificador da conta de origem (0 a 99)
    conta_origem = str(conta_origem).zfill(2)
    # Identificador da conta de destino (0 a 99)
    conta_destino = str(conta_destino).zfill(2)
    valor = str(valor).zfill(11)  # Valor da transferência (0 a 99999999999)
    return (msg_id + SEPARATOR + process_id + SEPARATOR + conta_origem + SEPARATOR + conta_destino + SEPARATOR + valor).zfill(F)
