@echo off
REM Script de configuração do projeto Resumidor de Vídeos do YouTube para Windows
REM Este script automatiza a instalação e configuração inicial

echo 🎬 Configurando Resumidor de Vídeos do YouTube...

REM Verificar se Python está instalado
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python não encontrado. Instale Python 3.8+ primeiro.
    pause
    exit /b 1
)

REM Mostrar versão do Python
echo ✅ Python detectado:
python --version

REM Criar ambiente virtual
echo 📦 Criando ambiente virtual...
python -m venv venv

REM Ativar ambiente virtual
echo 🔧 Ativando ambiente virtual...
call venv\Scripts\activate.bat

REM Atualizar pip
echo ⬆️ Atualizando pip...
python -m pip install --upgrade pip

REM Instalar dependências
echo 📚 Instalando dependências...
pip install -r requirements.txt

REM Copiar arquivo de configuração de exemplo
if not exist .env (
    echo 📝 Criando arquivo de configuração...
    copy .env.example .env
    echo ⚠️ Configure suas credenciais no arquivo .env
) else (
    echo ✅ Arquivo .env já existe
)

REM Verificar se FFmpeg está disponível
ffmpeg -version >nul 2>&1
if errorlevel 1 (
    echo ⚠️ FFmpeg não encontrado no PATH
    echo    Baixe em: https://ffmpeg.org/download.html
    
    REM Verificar se ffmpeg.exe existe localmente
    if exist ffmpeg.exe (
        echo ✅ FFmpeg local encontrado (ffmpeg.exe)
    )
) else (
    echo ✅ FFmpeg encontrado no PATH
)

REM Verificar suporte a GPU
echo 🔍 Verificando suporte a GPU...
python -c "import torch; print('✅ CUDA disponível - GPU detectada' if torch.cuda.is_available() else '⚠️ CUDA não disponível - usando CPU'); print(f'   Dispositivos: {torch.cuda.device_count()}' if torch.cuda.is_available() else ''); print(f'   GPU: {torch.cuda.get_device_name()}' if torch.cuda.is_available() else '')"

echo.
echo 🎉 Configuração concluída!
echo.
echo Próximos passos:
echo 1. Configure sua chave API do Gemini no arquivo .env
echo 2. Execute: python main.py
echo 3. Acesse: http://localhost:8000
echo.
echo Para mais informações, consulte o README.md

pause
