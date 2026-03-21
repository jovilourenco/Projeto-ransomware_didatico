# Projeto Ransomware Didático (RSA-2048)

Este projeto é uma ferramenta educacional desenvolvida para demonstrar o funcionamento técnico de um ataque de ransomware e a eficácia da criptografia híbrida (Sinuosa + Assimétrica) na prevenção da recuperação de arquivos sem a chave correta.

> [!WARNING]
> **AVISO LEGAL:** Este projeto foi criado estritamente para fins didáticos e educacionais. O uso deste software para atividades maliciosas em sistemas de terceiros sem autorização explícita é ilegal e antiético.

## 🚀 Como Funciona

O projeto utiliza um sistema de **criptografia híbrida**:
1.  **Criptografia Simétrica (AES/Fernet):** Usada para criptografar os arquivos reais de forma rápida e eficiente.
2.  **Criptografia Assimétrica (RSA-2048):** Usada para proteger a chave simétrica. A chave pública criptografa a chave AES (que criptograda os arquivos), e apenas a chave privada correspondente pode descriptografá-la.

Desta forma, mesmo que a vítima tenha acesso ao código do ransomware, ela não consegue descriptografar os arquivos sem a **chave privada** que permanece com o atacante.

## 📂 Estrutura do Projeto

Atacante:

*   `generate_keys.py`: Código auxiliar para gerar o par de chaves RSA-2048 (`public_key.pem` (no cliente) e `private_key.pem`).
*   `server.py`: Arquivo que inicia o servidor e fica "escutando" qualquer execução do ransomware. Ele quem recebe a chave AES criptografada e a retorna descriptografada (Repassada quando a vítima "pagar" o resgate).

Vítima:

*   `ransomware.py`: O script que localiza arquivos (atualmente limitados a certos Mime types para segurança), gera uma chave de sessão, criptografa os arquivos com chave AES, criptografa a chave AES com RSA 2048 e envia para o hacker.
*   `client.py`: Código auxiliar utilizado quando o cliente executar o ransomware. Ele que fará a conexão para enviar a chave AES criptografada para o atacante.
*   `alert_show.py`: Código auxiliar utilizado para exibir um alerta à vítima.
*   `decrypter.py`: Cria uma pequena interface para que a vítima (após contato e pagamento de resgate) insira a chave AES para descriptografar os arquivos.

## 🛠️ Pré-requisitos

*   Python 3.x
*   Biblioteca `cryptography`

Instale as dependências com:
```bash
pip install cryptography
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

## 🧪 Demonstração de Falha (O "Ataque" Real)

Para demonstrar que a recuperação é impossível sem a chave privada correta:

1.  Crie arquivos na pasta `arquivos_teste/`.
2.  Gere as chaves (`python generate_keys.py`).
3.  Execute o servidor (`python server.py`).
4.  Criptografe os arquivos (`python ransomware.py`).
5.  Gere as chaves novamente (`python generate_keys.py`).
6.  Execute o decrypter (`python decrypter.py`).
7.  Insira uma chave qualquer no decrypter.
8.  **Resultado:** O script falhará em descriptografar os arquivos, pois a nova chave privada não consegue abrir a chave de sessão protegida pela chave pública antiga.

## 🤖 Scripts de Automação (Windows)

Para facilitar a demonstração, você pode usar os scripts em lote fornecidos:

*   `teste_sucesso.bat`: Executa o fluxo completo e restaura os arquivos.
*   `teste_falha.bat`: Demonstra a impossibilidade de recuperação ao trocar de chaves.

---
Desenvolvido para fins de estudo sobre segurança da informação.
