#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Sistema de Gerenciamento com Menu Interativo
"""

import os
import sys
from config import PROJECT_ROOT
from usuarios.auth import AuthSystem

# Adiciona o diretório raiz ao path
sys.path.insert(0, PROJECT_ROOT)

class MenuPrincipal:
    def __init__(self):
        self.auth = AuthSystem()
        self.usuario_logado = None

    def limpar_tela(self):
        """Limpa a tela do console"""
        os.system('cls' if os.name == 'nt' else 'clear')

    def exibir_banner(self):
        """Exibe o banner inicial"""
        print("=" * 60)
        print(" " * 15 + "SECURE CHAIN AUDIT")
        print("=" * 60)

    def menu_principal(self):
        """Menu principal do sistema"""
        while True:
            self.limpar_tela()
            self.exibir_banner()
            
            if self.usuario_logado:
                print(f"\nConectado como: {self.usuario_logado['username']} ({self.usuario_logado['profile']})")
                print("\n" + "-" * 60)
                print("1. Criar novo usuário")
                print("2. Listar usuários")
                print("3. Deletar usuário")
                print("4. Logout")
                print("5. Sair")
                print("-" * 60)
            else:
                print("\nNenhum usuário conectado")
                print("\n" + "-" * 60)
                print("1. Fazer login")
                print("2. Criar novo usuário")
                print("3. Sair")
                print("-" * 60)

            opcao = input("\nEscolha uma opção: ").strip()

            if self.usuario_logado:
                if opcao == "1":
                    self.criar_usuario()
                elif opcao == "2":
                    self.listar_usuarios()
                elif opcao == "3":
                    self.deletar_usuario()
                elif opcao == "4":
                    self.logout()
                elif opcao == "5":
                    self.sair()
                else:
                    input("Opção inválida! Pressione Enter para continuar...")
            else:
                if opcao == "1":
                    self.fazer_login()
                elif opcao == "2":
                    self.criar_usuario()
                elif opcao == "3":
                    self.sair()
                else:
                    input("Opção inválida! Pressione Enter para continuar...")

    def fazer_login(self):
        """Realiza o login do usuário"""
        self.limpar_tela()
        self.exibir_banner()
        print("\n--- LOGIN ---\n")

        username = input("Usuário: ").strip()
        password = input("Senha: ").strip()

        user, mensagem = self.auth.login(username, password)

        if user:
            self.usuario_logado = user
            print(f"\n{mensagem}")
        else:
            print(f"\n{mensagem}")

        input("\nPressione Enter para continuar...")

    def criar_usuario(self):
        """Cria um novo usuário"""
        self.limpar_tela()
        self.exibir_banner()
        print("\n--- CRIAR NOVO USUÁRIO ---\n")

        username = input("Usuário: ").strip()
        password = input("Senha: ").strip()
        
        print("\nPerfis disponíveis:")
        print("1. admin (Administrador)")
        print("2. analista (Analista)")
        print("3. visitante (Visitante)")
        
        perfil_opcao = input("\nEscolha o perfil (1-3): ").strip()
        
        perfis = {
            "1": "admin",
            "2": "analista",
            "3": "visitante"
        }

        if perfil_opcao not in perfis:
            print("\nPerfil inválido!")
            input("Pressione Enter para continuar...")
            return

        perfil = perfis[perfil_opcao]

        # Validações básicas
        if not username or not password:
            print("\nUsuário e senha não podem estar vazios!")
            input("Pressione Enter para continuar...")
            return

        if len(password) < 6:
            print("\nSenha deve ter pelo menos 6 caracteres!")
            input("Pressione Enter para continuar...")
            return

        sucesso, mensagem = self.auth.register_user(username, password, perfil)

        if sucesso:
            print(f"\n{mensagem}")
        else:
            print(f"\n{mensagem}")

        input("\nPressione Enter para continuar...")

    def listar_usuarios(self):
        """Lista todos os usuários cadastrados"""
        self.limpar_tela()
        self.exibir_banner()
        print("\n--- LISTAR USUÁRIOS ---\n")

        usuarios, mensagem = self.auth.list_users()

        if usuarios:
            print(f"Total de usuários: {len(usuarios)}\n")
            print("-" * 50)
            print(f"{'Usuário':<25} {'Perfil':<20}")
            print("-" * 50)
            
            for usuario in usuarios:
                print(f"{usuario['username']:<25} {usuario['profile']:<20}")
            
            print("-" * 50)
        else:
            print(f"ℹ {mensagem}")

        input("\nPressione Enter para continuar...")

    def deletar_usuario(self):
        """Deleta um usuário existente"""
        self.limpar_tela()
        self.exibir_banner()
        print("\n--- DELETAR USUÁRIO ---\n")

        # Proteção para não deletar o próprio usuário
        if self.usuario_logado['profile'] != 'admin':
            print("\nApenas administradores podem deletar usuários!")
            input("Pressione Enter para continuar...")
            return

        username = input("Usuário a deletar: ").strip()

        if username == self.usuario_logado['username']:
            print("\nVocê não pode deletar sua própria conta!")
            input("Pressione Enter para continuar...")
            return

        confirmacao = input(f"Tem certeza que deseja deletar o usuário '{username}'? (s/n): ").strip().lower()

        if confirmacao != 's':
            print("\nOperação cancelada.")
            input("Pressione Enter para continuar...")
            return

        sucesso, mensagem = self.auth.delete_user(username)

        if sucesso:
            print(f"\n{mensagem}")
        else:
            print(f"\n{mensagem}")

        input("\nPressione Enter para continuar...")

    def logout(self):
        """Faz logout do usuário"""
        self.usuario_logado = None
        print("\nLogout realizado com sucesso!")
        input("Pressione Enter para continuar...")

    def sair(self):
        """Sai do sistema"""
        self.limpar_tela()
        print("\n" + "=" * 60)
        print(" " * 20 + "Até logo!")
        print("=" * 60 + "\n")
        sys.exit(0)


def main():
    """Função principal"""
    try:
        menu = MenuPrincipal()
        menu.menu_principal()
    except KeyboardInterrupt:
        print("\n\nSistema interrompido pelo usuário.")
        sys.exit(0)
    except Exception as e:
        print(f"\nErro: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
