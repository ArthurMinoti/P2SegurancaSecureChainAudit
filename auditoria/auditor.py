import os
import sys
import subprocess
from datetime import datetime
 
BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)
 
sys.path.insert(0, BASE_DIR)
 
from blockchain.blockchain import Blockchain
 
RELATORIOS_DIR = os.path.join(
    BASE_DIR,
    "auditoria",
    "relatorios"
)
 
os.makedirs(
    RELATORIOS_DIR,
    exist_ok=True
)
 
data = datetime.now().strftime(
    "%Y%m%d_%H%M%S"
)
 
arquivo_relatorio = os.path.join(
    RELATORIOS_DIR,
    f"auditoria_{data}.txt"
)
 
def executar(comando):
 
    try:
 
        resultado = subprocess.run(
            comando,
            shell=True,
            capture_output=True,
            text=True
        )
 
        return resultado.stdout
 
    except Exception as erro:
 
        return f"ERRO: {erro}"
 
who_output = executar("who")
last_output = executar("last -n 10")
ss_output = executar("ss -tulpn")
ip_output = executar("ip a")
 
with open(
    arquivo_relatorio,
    "w",
    encoding="utf-8"
) as relatorio:
 
    relatorio.write(
        "===== RELATÓRIO DE AUDITORIA =====\n"
    )
 
    relatorio.write(
        f"Data: {datetime.now()}\n\n"
    )
 
    relatorio.write(
        "===== WHO =====\n"
    )
 
    relatorio.write(who_output)
 
    relatorio.write(
        "\n\n===== LAST =====\n"
    )
 
    relatorio.write(last_output)
 
    relatorio.write(
        "\n\n===== SS =====\n"
    )
 
    relatorio.write(ss_output)
 
    relatorio.write(
        "\n\n===== IP A =====\n"
    )
 
    relatorio.write(ip_output)
 
try:
 
    bc = Blockchain()
 
    bc.add_block(
        "RELATÓRIO DE AUDITORIA GERADO"
    )
 
except Exception as erro:
 
    print(
        f"Erro ao registrar auditoria na blockchain: {erro}"
    )
 
print(
    f"Relatório criado em:\n{arquivo_relatorio}"
)