@echo off
setlocal

set "ERP_ROOT=C:\Projetos\SistemaERP"
set "VENV_SCRIPTS=%ERP_ROOT%\venv\Scripts"
set "DJANGO_DIR=%ERP_ROOT%\pedidos-api"
set "SPRING_DIR=C:\Projetos\SistemaFinanceiro"
set "FINANCEIRO_DIR=%ERP_ROOT%\Financeiro"

cls
echo =========================================================
echo Iniciando sistema financeiro...
echo =========================================================
echo.
echo Ativando ambiente virtual...
call "%VENV_SCRIPTS%\activate.bat"

if errorlevel 1 (
    echo Falha ao ativar o ambiente virtual.
    exit /b 1
)

echo.
echo Iniciando API Django (pedidos-api)...
start "Django API" /D "%DJANGO_DIR%" cmd /k "call %VENV_SCRIPTS%\activate.bat && python manage.py runserver"

set "DJANGO_OK=0"
echo Aguardando a API Django responder na porta 8000...
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
    echo API Django iniciada com sucesso.
) else (
    echo Atenção: a API Django ainda nao respondeu na porta 8000.
)

echo.
echo Iniciando API Spring Boot...
start "Spring Boot API" /D "%SPRING_DIR%" cmd /k "mvnw.cmd spring-boot:run"

set "SPRING_OK=0"
echo Aguardando a API Spring Boot responder na porta 8080...
for /L %%i in (1,1,30) do (
    powershell -NoProfile -Command "$ErrorActionPreference='SilentlyContinue'; try { Invoke-WebRequest -Uri 'http://127.0.0.1:8080/' -UseBasicParsing | Out-Null; exit 0 } catch { exit 1 }" >nul 2>&1
    if not errorlevel 1 (
        set "SPRING_OK=1"
        goto spring_ready
    )
    timeout /t 2 /nobreak >nul
)
:spring_ready

if "%SPRING_OK%"=="1" (
    echo API Spring Boot iniciada com sucesso.
) else (
    echo Atenção: a API Spring Boot ainda nao respondeu na porta 8080.
)

echo.
echo Iniciando aplicativo financeiro...
start "Aplicativo Financeiro" /D "%FINANCEIRO_DIR%" cmd /k "call %VENV_SCRIPTS%\activate.bat && py app.py"

echo.
echo =========================================================
echo Sistema inicializado.
echo - Django: http://127.0.0.1:8000
if "%SPRING_OK%"=="1" (
echo - Spring Boot: http://127.0.0.1:8080
) else (
echo - Spring Boot: aguardando inicializacao
)
echo - App Financeiro: janela aberta

echo =========================================================
endlocal
