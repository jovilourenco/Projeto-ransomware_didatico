@echo off
echo === DEMONSTRACAO DE SUCESSO ===
echo.

if not exist arquivos_teste mkdir arquivos_teste
echo Este e um documento importante > arquivos_teste\sucesso.txt
echo Imagem fake > arquivos_teste\foto.png

echo 1. Gerando chaves RSA...
python generate_keys.py

echo 2. Criptografando arquivos...
python ransomware.py

echo.
echo === ARQUIVOS CRIPTOGRAFADOS (Verifique a pasta agora) ===
echo Note que os arquivos originais sumiram e apenas .enc e key.bin.enc restam.
dir /b arquivos_teste
echo.
pause

echo 3. Descriptografando com a chave correta...
python decrypter.py

echo.
echo === ARQUIVOS APOS DESCRIPTOGRAFIA ===
dir /b arquivos_teste
echo.
type arquivos_teste\sucesso.txt
echo.
echo === TESTE CONCLUIDO COM SUCESSO ===
pause
