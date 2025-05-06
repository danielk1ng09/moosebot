@echo off
:loop
echo Cerrando ngrok viejo...
taskkill /IM ngrok.exe /F

timeout /t 2 /nobreak > NUL

echo Iniciando nuevo ngrok...
start "" ngrok.exe http 5000

echo Esperando 1 hora 50 minutos para reiniciar...
timeout /t 6600 /nobreak

goto loop
