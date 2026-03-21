import os
import threading
import base64
import tkinter as tk
from tkinter import messagebox
from cryptography.fernet import Fernet

files = []
dirs = []

def listdir(path): 
    try:
        for file in os.listdir(path):
            if os.path.isdir(f"{path}{file}"):
                dirs.append(f"{path}{file}/")
            elif file.split(".")[-1] == "enc" and file != "key.bin.enc":
                files.append(f"{path}{file}")
    except PermissionError:
        pass

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
        print(f"Erro ao descriptografar {file}: Chave inválida.")

# Lógica da Interface
def iniciar_decriptacao():
    chave_recebida = entry_key.get().strip()
    
    if not chave_recebida:
        messagebox.showwarning("Aviso", "Insira a chave recebida do servidor.")
        return

    try:
        # Como o servidor retorna a string da chave codificada em base64, 
        # precisamos decodificá-la uma vez para obter a chave Fernet real.
        chave_final = base64.b64decode(chave_recebida)
        
        # Valida se a chave resultante é aceita pelo Fernet
        Fernet(chave_final)
    except Exception:
        messagebox.showerror("Erro", "A chave inserida é inválida ou não está no formato esperado.")
        return

    # Executa a lógica de listagem dos arquivos no diretório.
    files.clear()
    dirs.clear()
    listdir("./")

    if len(dirs) > 0:
        threads_dir = []
        for d in dirs:
            t = threading.Thread(target=listdir, args=(d,))
            threads_dir.append(t)
            t.start()
        for t in threads_dir:
            t.join()

    # Executa a descriptografia
    threads_dec = []
    for file in files:
        t = threading.Thread(target=decrypt, args=(file, chave_final))
        threads_dec.append(t)
        t.start()
    
    for t in threads_dec:
        t.join()

    messagebox.showinfo("Sucesso", "Arquivos descriptografados com sucesso!")

# Somente monta uma interface simples com o TKinter
root = tk.Tk()
root.title("Decriptador Acadêmico")
root.geometry("500x200")

tk.Label(root, text="Coloque a chave recebida aqui:", pady=10, font=("Arial", 10)).pack()

entry_key = tk.Entry(root, width=60, font=("Courier", 9))
entry_key.pack(padx=20, pady=5)

btn = tk.Button(root, text="Descriptografar arquivos", command=iniciar_decriptacao, 
                bg="#d32f2f", fg="white", font=("Arial", 10, "bold"), padx=20, pady=10)
btn.pack(pady=20)

root.mainloop()