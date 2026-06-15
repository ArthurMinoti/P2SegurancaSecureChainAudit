import hashlib
import json
import os
import sys
from datetime import datetime

# Adiciona o diretório pai ao path para importações
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config import CHAIN_FILE


class Block:
    def __init__(self, index, timestamp, event, previous_hash, hash=None):
        self.index = index
        self.timestamp = timestamp
        self.event = event
        self.previous_hash = previous_hash
        self.hash = hash or self.calculate_hash()

    def calculate_hash(self):
        block_string = json.dumps(
            {
                "index": self.index,
                "timestamp": self.timestamp,
                "event": self.event,
                "previous_hash": self.previous_hash,
            },
            sort_keys=True,
        ).encode()
        return hashlib.sha256(block_string).hexdigest()

    def to_dict(self):
        return {
            "index": self.index,
            "timestamp": self.timestamp,
            "event": self.event,
            "previous_hash": self.previous_hash,
            "hash": self.hash,
        }


class Blockchain:
    def __init__(self, chain_file=CHAIN_FILE):
        self.chain_file = chain_file
        self.chain = self.load_chain()

    def load_chain(self):
        if os.path.exists(self.chain_file):
            try:
                with open(self.chain_file, "r") as f:
                    data = json.load(f)
                    if not data:
                        return [self.create_genesis_block()]
                    return [Block(**b) for b in data]
            except (json.JSONDecodeError, TypeError):
                return [self.create_genesis_block()]
        return [self.create_genesis_block()]

    def create_genesis_block(self):
        genesis_block = Block(
            0,
            datetime.now().isoformat(),
            "Genesis Block - SecureChain Audit Initialized",
            "0",
        )
        self.save_chain([genesis_block])
        return genesis_block

    def save_chain(self, chain=None):
        if chain is None:
            chain = self.chain
        with open(self.chain_file, "w") as f:
            # Garante que estamos salvando uma lista de dicionários
            data_to_save = []
            for block in chain:
                if isinstance(block, Block):
                    data_to_save.append(block.to_dict())
                else:
                    data_to_save.append(block)
            json.dump(data_to_save, f, indent=4)

    def get_latest_block(self):
        return self.chain[-1]

    def add_block(self, event):
        latest_block = self.get_latest_block()
        new_block = Block(
            index=latest_block.index + 1,
            timestamp=datetime.now().isoformat(),
            event=event,
            previous_hash=latest_block.hash,
        )
        self.chain.append(new_block)
        self.save_chain(self.chain)
        return new_block

    def is_chain_valid(self):
        for i in range(1, len(self.chain)):
            current = self.chain[i]
            previous = self.chain[i - 1]

            # Valida hash do bloco atual
            if current.hash != current.calculate_hash():
                return False, i, "Hash do bloco adulterado"

            # Valida encadeamento
            if current.previous_hash != previous.hash:
                return False, i, "Quebra de encadeamento"

        return True, None, "Blockchain íntegra"


    def print_chain(self):

        print("\n" + "=" * 80)
        print("BLOCKCHAIN DE AUDITORIA")
        print("=" * 80)
        for block in self.chain:
            print(f"\nID: {block.index}")
            print(f"Timestamp: {block.timestamp}")
            print(f"Evento: {block.event}")
            print(f"Hash Anterior: {block.previous_hash}")
            print(f"Hash Atual: {block.hash}")
            print("-" * 80)


if __name__ == "__main__":
    bc = Blockchain()
    print(f"Blockchain carregada com {len(bc.chain)} blocos.")
    valid, index, msg = bc.is_chain_valid()
    print(f"Status: {msg}")
