@echo off
cd /d "E:\Dropbox\4. Heres Logistic\0. Moose Machinery Group\12 IA Whatsapp\7. Twilio"

echo Iniciando servidor Flask...
start "Flask" cmd /k "python app.py"

timeout /t 3 >nul

echo Iniciando Ngrok...
start "Ngrok" cmd /k "ngrok http 5000"

timeout /t 3 >nul

echo ✅ Flask y Ngrok iniciados. Copia manualmente la URL pública de la ventana de Ngrok.
echo 🔗 Recuerda agregar /webhook al final antes de pegarla en Twilio.
pause
