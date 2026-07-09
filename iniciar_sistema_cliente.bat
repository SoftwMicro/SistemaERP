@echo off
setlocal

set "ERP_ROOT=C:\Projetos\SistemaERP"
set "VENV_SCRIPTS=%ERP_ROOT%\venv\Scripts"
set "DJANGO_DIR=%ERP_ROOT%\pedidos-api"
set "CLIENTE_DIR=%ERP_ROOT%\cliente"

cls
echo =========================================================
echo Iniciando Sistema Cliente...
echo =========================================================
echo.
echo Ativando ambiente virtual...
call "%VENV_SCRIPTS%\activate.bat"

if errorlevel 1 (
    echo Falha ao ativar o ambiente virtual.
    exit /b 1
)

echo.
echo Iniciando API de pedidos...
start "API Pedidos" /D "%DJANGO_DIR%" cmd /k "call %VENV_SCRIPTS%\activate.bat && python manage.py runserver"

set "DJANGO_OK=0"
echo Aguardando a API responder na porta 8000...
for /L %%i in (1,1,30) do (
    powershell -NoProfile -Command "$ErrorActionPreference='SilentlyContinue'; try { Invoke-WebRequest -Uri 'http://127.0.0.1:8000/' -UseBasicParsing | Out-Null; exit 0 } catch { exit 1 }" >nul 2>&1
    if not errorlevel 1 (
        set "DJANGO_OK=1"
        goto django_ready
    )
    timeout /t 2 /nobreak >nul
)
:django_ready

if "%DJANGO_OK%"=="1" (
    echo API de pedidos iniciada com sucesso.
) else (
    echo Atenção: a API ainda nao respondeu na porta 8000.
)

echo.
echo Iniciando aplicativo cliente...
start "Sistema Cliente" /D "%CLIENTE_DIR%" cmd /k "call %VENV_SCRIPTS%\activate.bat && py app.py"

echo.
echo =========================================================
echo Sistema Cliente inicializado.
echo - API Pedidos: http://127.0.0.1:8000
echo - Aplicativo Cliente: janela aberta

echo =========================================================
endlocal
