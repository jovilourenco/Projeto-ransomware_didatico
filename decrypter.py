from cryptography.fernet import Fernet
import os
import threading
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import padding

def decrypt(file, key):
    try:
        fernet = Fernet(key)

        with open(file, "rb") as f:
            enc_data = f.read()

        data = fernet.decrypt(enc_data)

        with open(file.replace(".enc", ""), "wb") as f:
            f.write(data)
            os.remove(file)
    except Exception as e:
        print(f"Erro ao descriptografar {file}: Chave incorreta ou arquivo corrompido.")

def listdir(path): # Irá listar os diretórios recursivamente até encontrar todos os arquivos.
    try:
        for file in os.listdir(path):
            if os.path.isdir(f"{path}{file}"):
                dirs.append(f"{path}{file}/")
            elif file.split(".")[-1] == "enc" and file != "key.bin.enc": # Ignora o proprio arquivo de chave
                files.append(f"{path}{file}")

    except PermissionError:
        None

files = []
dirs = []
listdir("./")

if len(dirs) > 0:
    threads = []
    for dir in dirs:
        t = threading.Thread(target=listdir, args=(dir,))
        threads.append(t)
        t.start()
    
    for t in threads:
        t.join()

# Carregar chave privada RSA
with open("private_key.pem", "rb") as f:
    private_key = serialization.load_pem_private_key(
        f.read(),
        password=None
    )

# Carregar e descriptografar a chave Fernet
with open("key.bin.enc", "rb") as f:
    enc_key = f.read()

key = private_key.decrypt(
    enc_key,
    padding.OAEP(
        mgf=padding.MGF1(algorithm=hashes.SHA256()),
        algorithm=hashes.SHA256(),
        label=None
    )
)

for file in files:
    t = threading.Thread(target=decrypt, args=(file, key,))
    t.start()

