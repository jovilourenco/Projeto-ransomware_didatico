from cryptography.fernet import Fernet
import os
import threading

def decrypt(file, key):
    try:
        fernet = Fernet(key)

        with open(file, "rb") as f:
            enc_data = f.read()

        data = fernet.decrypt(enc_data)

        with open(file.replace(".enc", ""), "wb") as f:
            f.write(data)
            os.remove(file)
    except:
        None

def listdir(path): # Irá listar os diretórios recursivamente até encontrar todos os arquivos.
    try:
        for file in os.listdir(path):
            if os.path.isdir(f"{path}{file}"):
                dirs.append(f"{path}{file}/")
            elif file.split(".")[-1] == "enc": # A diferença é que não precisamos de checkfile. Se o arquivo for .enc, já sabemos que queremos descriptá-lo
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

key = b'apJsqTlydjIq36mPlDyURQ1Ebi5HyTLqMLOprTZjsgM=' # Aqui vai a chave gerada no console ao rodar o ecripter
for file in files:
    t = threading.Thread(target=decrypt, args=(file, key,))
    t.start()

