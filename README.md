1. Importar Debian 13 do OneDrive.

2. Este projeto utiliza uma máquina virtual Debian previamente configurada.

A VM já contém:
- Git
- Python 3
- OpenSSL
- Nmap
- Tree
- Net-tools

3. Configura Git: (exemplo)
git config --global user.name "Arthur"
git config --global user.email "emailGithub"

4. Clonar o repositório:
git clone ... (link do repo)

5. Entrar na pasta:
cd P2SegurancaSecureChainAudit

6. Atualizar a branch main:
git checkout main
git pull origin main

teste com o comando tree para ver se puxou todos os diretorios e arquivos.

7. Criar seu branch pessoal com o nome feature/nomedafeature-seunome (eu por exemplo farei
o blockchain, portanto "feature/blockchain-lucas")

8. Criar ambiente virtual:
python3 -m venv venv

9. Ativar:
source venv/bin/activate

10. Instalar dependências:
pip install -r requirements.txt

ou

pip install bcrypt
pip freeze > requirements.txt

11. Criar grupo e usuários Linux:
cd ..

sudo groupadd securechain

sudo useradd -m -G securechain administrador
sudo passwd administrador     ----> (admin)

sudo useradd -m -G securechain analista
sudo passwd analista           ----> (analista)

sudo useradd -m visitante
sudo passwd visitante           ----> (visit)

12. Permissões

Adiciona seu usuario ao grupo:
sudo usermod -aG securechain vboxuser

Demais permissões:
sudo chown -R vboxuser:securechain ~/P2SegurancaSecureChainAudit

chmod -R 755 P2SegurancaSecureChainAudit/auditoria/relatorios

chmod -R 770 ~/P2SegurancaSecureChainAudit

chmod g+s ~/P2SegurancaSecureChainAudit

13. Continue de acordo com sua parte do projeto, faça as mudanças, commit e depois push
utilizando Token PAT como senha do github (gerado no proprio github, em configurações do desenvolvedor)


