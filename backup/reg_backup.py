import os
import sys
 
BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)
 
sys.path.insert(0, BASE_DIR)
 
from blockchain.blockchain import Blockchain
 
try:
 
    blockchain = Blockchain()
 
    blockchain.add_block(
        "BACKUP EXECUTADO COM SUCESSO"
    )
 
    print(
        "Evento de backup registrado na blockchain."
    )
 
except Exception as erro:
 
    print(
        f"Erro ao registrar backup: {erro}"
    )