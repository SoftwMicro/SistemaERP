@echo off
setlocal

set "ERP_ROOT=C:\Projetos\SistemaERP"
set "VENV_ACTIVATE=%ERP_ROOT%\venv\Scripts\Activate.ps1"
set "POS_DIR=%ERP_ROOT%\Pos"

if not exist "%VENV_ACTIVATE%" (
    echo Arquivo de ativacao do ambiente virtual nao encontrado: "%VENV_ACTIVATE%"
    exit /b 1
)

if not exist "%POS_DIR%" (
    echo Diretorio do POS nao encontrado: "%POS_DIR%"
    exit /b 1
)

echo =========================================================
echo Iniciando sistema POS...
echo =========================================================
echo.
echo Ativando ambiente virtual...
powershell -NoProfile -ExecutionPolicy Bypass -Command "& '%VENV_ACTIVATE%'; Set-Location '%POS_DIR%'; py app.py"

endlocal
