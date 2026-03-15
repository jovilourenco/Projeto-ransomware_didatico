# Projeto Ransomware Didático (RSA-2048)

Este projeto é uma ferramenta educacional desenvolvida para demonstrar o funcionamento técnico de um ataque de ransomware e a eficácia da criptografia híbrida (Sinuosa + Assimétrica) na prevenção da recuperação de arquivos sem a chave correta.

> [!WARNING]
> **AVISO LEGAL:** Este projeto foi criado estritamente para fins didáticos e educacionais. O uso deste software para atividades maliciosas em sistemas de terceiros sem autorização explícita é ilegal e antiético.

## 🚀 Como Funciona

O projeto utiliza um sistema de **criptografia híbrida**:
1.  **Criptografia Simétrica (AES/Fernet):** Usada para criptografar os arquivos reais de forma rápida e eficiente.
2.  **Criptografia Assimétrica (RSA-2048):** Usada para proteger a chave simétrica. A chave pública criptografa a chave de sessão, e apenas a chave privada correspondente pode descriptografá-la.

Desta forma, mesmo que a vítima tenha acesso ao código do ransomware, ela não consegue descriptografar os arquivos sem a **chave privada** que permanece com o atacante.

## 📂 Estrutura do Projeto

*   `generate_keys.py`: Gera o par de chaves RSA-2048 (`public_key.pem` e `private_key.pem`).
*   `ransomware.py`: O script que localiza arquivos (atualmente limitados a `.pdf` para segurança), gera uma chave de sessão, criptografa os arquivos e protege a chave com RSA.
*   `decrypter.py`: Utiliza a chave privada para recuperar a chave de sessão e descriptografar os arquivos.
*   `teste.pdf`: Arquivo de teste fornecido para demonstração.

## 🛠️ Pré-requisitos

*   Python 3.x
*   Biblioteca `cryptography`

Instale as dependências com:
```bash
pip install cryptography
```

## 📖 Passo a Passo de Uso

1.  **Gerar Chaves:**
    ```bash
    python generate_keys.py
    ```
    Isso criará os arquivos `.pem`. Em um cenário real, a `private_key.pem` nunca sairia da máquina do atacante.

2.  **Criptografar:**
    ```bash
    python ransomware.py
    ```
    Os arquivos `.pdf` na pasta serão substituídos por versões `.enc` e uma chave protegida `key.bin.enc` será gerada.

3.  **Descriptografar:**
    ```bash
    python decrypter.py
    ```
    Usando a chave privada, os arquivos originais serão restaurados.

## 🧪 Demonstração de Falha (O "Ataque" Real)

Para demonstrar que a recuperação é impossível sem a chave privada correta:

1.  Crie arquivos na pasta `arquivos_teste/`.
2.  Gere as chaves (`python generate_keys.py`).
3.  Criptografe os arquivos (`python ransomware.py`).
4.  **Simule a perda da chave:** Renomeie o arquivo `private_key.pem` para `private_key_SECRET.pem`.
5.  **Gere novas chaves:** Execute `python generate_keys.py` novamente. Isso criará um **novo par** de chaves que não tem relação com os arquivos já criptografados.
6.  **Tente descriptografar:** Execute `python decrypter.py`.
7.  **Resultado:** O script falhará em descriptografar os arquivos, pois a nova chave privada não consegue abrir a chave de sessão protegida pela chave pública antiga.

## 🤖 Scripts de Automação (Windows)

Para facilitar a demonstração, você pode usar os scripts em lote fornecidos:

*   `teste_sucesso.bat`: Executa o fluxo completo e restaura os arquivos.
*   `teste_falha.bat`: Demonstra a impossibilidade de recuperação ao trocar de chaves.

---
Desenvolvido para fins de estudo sobre segurança da informação.
