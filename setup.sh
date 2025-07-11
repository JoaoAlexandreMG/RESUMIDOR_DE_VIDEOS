#!/bin/bash

# Script de configuração do projeto Resumidor de Vídeos do YouTube
# Este script automatiza a instalação e configuração inicial

echo "🎬 Configurando Resumidor de Vídeos do YouTube..."

# Verificar se Python está instalado
if ! command -v python &> /dev/null; then
    echo "❌ Python não encontrado. Instale Python 3.8+ primeiro."
    exit 1
fi

# Verificar versão do Python
python_version=$(python -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')")
echo "✅ Python $python_version detectado"

# Criar ambiente virtual
echo "📦 Criando ambiente virtual..."
python -m venv venv

# Ativar ambiente virtual
echo "🔧 Ativando ambiente virtual..."
if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "win32" ]]; then
    source venv/Scripts/activate
else
    source venv/bin/activate
fi

# Atualizar pip
echo "⬆️ Atualizando pip..."
pip install --upgrade pip

# Instalar dependências
echo "📚 Instalando dependências..."
pip install -r requirements.txt

# Copiar arquivo de configuração de exemplo
if [ ! -f .env ]; then
    echo "📝 Criando arquivo de configuração..."
    cp .env.example .env
    echo "⚠️ Configure suas credenciais no arquivo .env"
else
    echo "✅ Arquivo .env já existe"
fi

# Verificar se FFmpeg está instalado
if ! command -v ffmpeg &> /dev/null; then
    echo "⚠️ FFmpeg não encontrado no PATH"
    echo "   Baixe em: https://ffmpeg.org/download.html"
    
    # Se estiver no Windows e ffmpeg.exe existir localmente
    if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "win32" ]] && [ -f ffmpeg.exe ]; then
        echo "✅ FFmpeg local encontrado (ffmpeg.exe)"
    fi
else
    echo "✅ FFmpeg encontrado"
fi

# Verificar se PyTorch suporta CUDA
echo "🔍 Verificando suporte a GPU..."
python -c "
import torch
if torch.cuda.is_available():
    print('✅ CUDA disponível - GPU detectada')
    print(f'   Dispositivos: {torch.cuda.device_count()}')
    print(f'   GPU: {torch.cuda.get_device_name()}')
else:
    print('⚠️ CUDA não disponível - usando CPU')
"

echo ""
echo "🎉 Configuração concluída!"
echo ""
echo "Próximos passos:"
echo "1. Configure sua chave API do Gemini no arquivo .env"
echo "2. Execute: python main.py"
echo "3. Acesse: http://localhost:8000"
echo ""
echo "Para mais informações, consulte o README.md"
