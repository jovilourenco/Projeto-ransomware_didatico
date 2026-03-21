@echo off
echo === DEMONSTRACAO DE FALHA (CHAVE INCORRETA) ===
echo.

if not exist arquivos_teste mkdir arquivos_teste
echo Documento confidencial > arquivos_teste\segredo.txt

echo 1. Gerando chaves RSA originais...
python generate_keys.py

echo 2. Criptografando arquivos...
python ransomware.py

echo.
echo === ARQUIVOS CRIPTOGRAFADOS ===
echo Verifique que os arquivos estao protegidos antes de perdermos a chave.
dir /b arquivos_teste
echo.
pause

echo 3. Simulando perda da chave privada original...
move private_key.pem private_key_ORIGINAL.pem

echo 4. Gerando NOVO par de chaves (Atacante perdeu a original ou voce esta usando a errada)...
python generate_keys.py

echo 5. Tentando descriptografar com a chave NOVA (Incorreta)...
python decrypter.py

echo.
echo === RESULTADO ===
echo Os arquivos nao devem ter sido restaurados.
dir /b arquivos_teste
echo.
pause

echo 6. Restaurando chave original para permitir recuperacao futura...
del private_key.pem
move private_key_ORIGINAL.pem private_key.pem

echo.
echo 7. Tentando descriptografar agora com a chave CORRETA...
python decrypter.py

echo.
echo === RESULTADO FINAL ===
echo Os arquivos devem ter sido restaurados agora.
dir /b arquivos_teste
echo.

echo === TESTE DE FALHA E RECUPERACAO CONCLUIDO ===
pause
