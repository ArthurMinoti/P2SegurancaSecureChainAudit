import os

# Caminhos globais do projeto
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
USERS_FOLDER = os.path.join(PROJECT_ROOT, 'usuarios')
DOCUMENTS_FOLDER = os.path.join(PROJECT_ROOT, 'documentos')
BLOCKCHAIN_FOLDER = os.path.join(PROJECT_ROOT, 'blockchain')
LOGS_FOLDER = os.path.join(PROJECT_ROOT,'logs')

USERS_DB = os.path.join(USERS_FOLDER, 'users.json')
HASH_DB = os.path.join(LOGS_FOLDER,'hashes.json')
HASH_DB = os.path.join(DOCUMENTS_FOLDER, 'hashes.json')
CHAIN_FILE = os.path.join(BLOCKCHAIN_FOLDER, 'chain.json')
