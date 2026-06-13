import bcrypt
import json
import os
import sys

# Adiciona o diretório pai ao path para importações
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config import USERS_DB
from blockchain.blockchain import Blockchain

class AuthSystem:
    def __init__(self, db_path=USERS_DB):
        self.db_path = db_path
        self.blockchain = Blockchain()
        self.users = self.load_users()

    def load_users(self):
        if os.path.exists(self.db_path):
            with open(self.db_path, 'r') as f:
                return json.load(f)
        return {}

    def save_users(self):
        with open(self.db_path, 'w') as f:
            json.dump(self.users, f, indent=4)

    def register_user(self, username, password, profile):
        if username in self.users:
            return False, "Usuário já existe."
        
        if profile not in ['admin', 'analista', 'visitante']:
            return False, "Perfil inválido."

        # Hash da senha com bcrypt
        salt = bcrypt.gensalt()
        hashed_pw = bcrypt.hashpw(password.encode(), salt).decode()

        self.users[username] = {
            "password": hashed_pw,
            "profile": profile
        }
        self.save_users()
        self.blockchain.add_block(f"Usuário criado: {username} (Perfil: {profile})")
        return True, f"Usuário {username} cadastrado com sucesso."

    def login(self, username, password):
        if username not in self.users:
            self.blockchain.add_block(f"Tentativa de login falha: Usuário {username} não encontrado.")
            return None, "Usuário ou senha incorretos."

        user_data = self.users[username]
        if bcrypt.checkpw(password.encode(), user_data['password'].encode()):
            self.blockchain.add_block(f"Login realizado: {username} (Perfil: {user_data['profile']})")
            return {"username": username, "profile": user_data['profile']}, "Login bem-sucedido."
        
        self.blockchain.add_block(f"Tentativa de login falha: Senha incorreta para {username}.")
        return None, "Usuário ou senha incorretos."

    def delete_user(self, username):
        if username not in self.users:
            return False, f"Usuário {username} não encontrado."
        
        del self.users[username]
        self.save_users()
        self.blockchain.add_block(f"Usuário deletado: {username}")
        return True, f"Usuário {username} deletado com sucesso."

    def list_users(self):
        if not self.users:
            return [], "Nenhum usuário cadastrado."
        
        users_list = []
        for username, data in self.users.items():
            users_list.append({
                "username": username,
                "profile": data['profile']
            })
        return users_list, "Usuários listados com sucesso."

if __name__ == "__main__":
    auth = AuthSystem()
    # Criar admin padrão se não existir
    if 'admin' not in auth.users:
        auth.register_user('admin', 'admin123', 'admin')
        print("Usuário admin padrão criado.")
    
    user, msg = auth.login('admin', 'admin123')
    print(f"Resultado do login: {msg} -> {user}")
