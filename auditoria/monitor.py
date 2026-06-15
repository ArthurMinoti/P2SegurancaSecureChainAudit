import os
import sys
import json
import time
import hashlib
from datetime import datetime

BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)

sys.path.insert(0, BASE_DIR)

from blockchain.blockchain import Blockchain

# Diretórios

DOCUMENTOS_DIR = os.path.join(BASE_DIR, "documentos")
LOGS_DIR = os.path.join(BASE_DIR, "logs")

HASH_FILE = os.path.join(LOGS_DIR, "hashes.json")
LOG_FILE = os.path.join(LOGS_DIR, "monitor.log")


class MonitorIntegridade:

    def __init__(self):

        self.blockchain = Blockchain()

        os.makedirs(LOGS_DIR, exist_ok=True)
        os.makedirs(DOCUMENTOS_DIR, exist_ok=True)

    def calcular_hash(self, arquivo):

        sha256 = hashlib.sha256()

        with open(arquivo, "rb") as f:

            while True:

                bloco = f.read(4096)

                if not bloco:
                    break

                sha256.update(bloco)

        return sha256.hexdigest()

    def gerar_hashes_atuais(self):

        hashes = {}

        for raiz, _, arquivos in os.walk(DOCUMENTOS_DIR):

            for arquivo in arquivos:

                caminho = os.path.join(raiz, arquivo)

                try:

                    hash_arquivo = self.calcular_hash(caminho)

                    caminho_relativo = os.path.relpath(
                        caminho,
                        DOCUMENTOS_DIR
                    )

                    hashes[caminho_relativo] = hash_arquivo

                except Exception as erro:

                    self.registrar_log(
                        f"Erro ao calcular hash de {arquivo}: {erro}"
                    )

        return hashes

    def carregar_hashes(self):

        if not os.path.exists(HASH_FILE):
            return {}

        try:

            with open(
                HASH_FILE,
                "r",
                encoding="utf-8"
            ) as arquivo:

                return json.load(arquivo)

        except Exception:

            return {}

    def salvar_hashes(self, hashes):

        with open(
            HASH_FILE,
            "w",
            encoding="utf-8"
        ) as arquivo:

            json.dump(
                hashes,
                arquivo,
                indent=4,
                ensure_ascii=False
            )

    def registrar_log(self, mensagem):

        timestamp = datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        )

        linha = f"[{timestamp}] {mensagem}"

        print(linha)

        with open(
            LOG_FILE,
            "a",
            encoding="utf-8"
        ) as log:

            log.write(linha + "\n")

    def gerar_alerta(self, evento):

        alerta = (
            "\n"
            "=====================================\n"
            " ALERTA DE INTEGRIDADE DETECTADO\n"
            f" {evento}\n"
            "====================================="
        )

        print(alerta)

        self.registrar_log(
            f"ALERTA: {evento}"
        )

    def registrar_evento(self, evento):

        self.registrar_log(evento)

        try:

            self.blockchain.add_block(evento)

        except Exception as erro:

            self.registrar_log(
                f"Erro ao registrar na blockchain: {erro}"
            )

    def inicializar(self):

        hashes = self.gerar_hashes_atuais()

        self.salvar_hashes(hashes)

        self.registrar_log(
            "Base inicial de hashes criada."
        )

    def verificar_integridade(self):

        self.registrar_log(
            "Executando verificação periódica."
        )

        hashes_antigos = self.carregar_hashes()

        hashes_atuais = self.gerar_hashes_atuais()

        #
        # ALTERAÇÃO
        #

        for arquivo, hash_antigo in hashes_antigos.items():

            if arquivo in hashes_atuais:

                hash_novo = hashes_atuais[arquivo]

                if hash_antigo != hash_novo:

                    evento = (
                        f"ARQUIVO ALTERADO: {arquivo}"
                    )

                    self.gerar_alerta(evento)

                    self.registrar_evento(evento)

        #
        # EXCLUSÃO
        #

        for arquivo in hashes_antigos:

            if arquivo not in hashes_atuais:

                evento = (
                    f"ARQUIVO REMOVIDO: {arquivo}"
                )

                self.gerar_alerta(evento)

                self.registrar_evento(evento)

        #
        # INCLUSÃO
        #

        for arquivo in hashes_atuais:

            if arquivo not in hashes_antigos:

                evento = (
                    f"NOVO ARQUIVO DETECTADO: {arquivo}"
                )

                self.gerar_alerta(evento)

                self.registrar_evento(evento)

        self.salvar_hashes(hashes_atuais)

    def executar(self):

        if not os.path.exists(HASH_FILE):

            self.inicializar()

        else:

            self.verificar_integridade()

    def monitorar_continuamente(self, intervalo=30):

        self.registrar_log(
            f"Monitoramento iniciado. Intervalo: {intervalo} segundos."
        )

        while True:

            self.executar()

            time.sleep(intervalo)


if __name__ == "__main__":

    monitor = MonitorIntegridade()

    monitor.monitorar_continuamente()
