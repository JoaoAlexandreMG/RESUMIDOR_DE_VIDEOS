# 🎬 Resumidor Inteligente de Vídeos do YouTube

Uma aplicação web moderna que baixa áudio de vídeos do YouTube, transcreve usando OpenAI Whisper e gera resumos inteligentes em HTML usando Google Gemini AI.

## 🌟 Funcionalidades

- 📥 **Download de áudio**: Extrai áudio de vídeos do YouTube automaticamente
- 🎙️ **Transcrição**: Usa OpenAI Whisper para converter áudio em texto com detecção automática de GPU
- 🤖 **Resumo inteligente**: Gera resumos personalizados usando Google Gemini 2.0 Flash
- 🎨 **Interface moderna**: Web app responsiva com design moderno
- 📱 **Mobile-friendly**: Interface adaptada para dispositivos móveis
- ⚡ **Processamento rápido**: Otimizado para performance com suporte a GPU
- 📄 **Export HTML**: Gera arquivos HTML prontos para visualização

## Interface Principal

A aplicação possui uma interface limpa e intuitiva onde você pode:

1. Colar o link do vídeo do YouTube
2. Fazer uma pergunta específica (opcional)
3. Receber um resumo em HTML formatado

## 🛠️ Tecnologias Utilizadas

- **Backend**: FastAPI (Python)
- **IA/ML**:
  - OpenAI Whisper (transcrição)
  - Google Gemini 2.0 Flash (resumo)
  - PyTorch (detecção de GPU)
- **Download**: yt-dlp
- **Frontend**: HTML/CSS/JavaScript (interface embedded)
- **Processamento**: FFmpeg

## 📋 Pré-requisitos

- Python 3.8+
- FFmpeg instalado no sistema
- GPU NVIDIA (opcional, para acelerar transcrição)
- Chave API do Google Gemini

## 🔧 Instalação

### 1. Clone o repositório

```bash
git clone https://github.com/seu-usuario/resumidor-videos-youtube.git
cd resumidor-videos-youtube
```

### 2. Instale as dependências

```bash
pip install -r requirements.txt
```

### 3. Configure as variáveis de ambiente

Crie um arquivo `.env` na raiz do projeto:

```env
GEMINI_API_KEY=sua_chave_api_aqui
```

### 4. Instale o FFmpeg

- **Windows**: Baixe do [site oficial](https://ffmpeg.org/download.html) e adicione ao PATH
- **Linux**: `sudo apt install ffmpeg`
- **macOS**: `brew install ffmpeg`

## 🚀 Como Usar

### 1. Inicie o servidor

```bash
python main.py
```

### 2. Acesse a aplicação

Abra seu navegador e vá para: `http://localhost:8000`

### 3. Use a aplicação

1. Cole o link de um vídeo do YouTube
2. (Opcional) Digite uma pergunta específica sobre o vídeo
3. Clique em "Analisar"
4. Aguarde o processamento e baixe o arquivo HTML gerado

## 🔧 Configuração Avançada

### Modelos Whisper Disponíveis

O projeto usa o modelo `tiny` por padrão para velocidade. Você pode alterar no código:

- `tiny`: Mais rápido, menor precisão
- `base`: Equilibrio entre velocidade e precisão
- `small`: Boa precisão, velocidade moderada
- `medium`: Alta precisão, mais lento
- `large`: Máxima precisão, mais lento

### GPU vs CPU

A aplicação detecta automaticamente se há GPU disponível:

- **Com GPU**: Transcrição muito mais rápida
- **Sem GPU**: Funciona normalmente, mas mais lento

## 📁 Estrutura do Projeto

```text
resumidor-videos-youtube/
├── main.py              # Aplicação principal FastAPI
├── requirements.txt     # Dependências Python
├── .env                # Variáveis de ambiente (criar)
├── ffmpeg.exe          # Executável FFmpeg (Windows)
├── README.md           # Este arquivo
├── CHANGELOG.md        # Histórico de versões
├── CONTRIBUTING.md     # Guia de contribuição
└── LICENSE            # Licença do projeto
```

## 🔌 API Endpoints

### `GET /`

Página principal da aplicação com interface web.

### `GET /analisar_video`

Processa um vídeo do YouTube e retorna resumo em HTML.

**Parâmetros:**

- `url` (string, obrigatório): URL do vídeo do YouTube
- `pergunta` (string, opcional): Pergunta específica sobre o vídeo

**Resposta:**

- Sucesso: Arquivo HTML para download
- Erro: JSON com detalhes do erro

## 🤝 Contribuindo

Contribuições são bem-vindas! Veja o [CONTRIBUTING.md](CONTRIBUTING.md) para detalhes.

### Como contribuir

1. Fork o projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## 📝 Licença

Este projeto está licenciado sob a Licença MIT - veja o arquivo [LICENSE](LICENSE) para detalhes.

## 🐛 Problemas Conhecidos

- Vídeos muito longos (>2h) podem causar timeout
- Alguns vídeos privados ou com restrição regional não funcionam
- A qualidade da transcrição depende da qualidade do áudio original

## 📞 Suporte

Se encontrar problemas:

1. Verifique os [issues existentes](https://github.com/seu-usuario/resumidor-videos-youtube/issues)
2. Crie um novo issue com detalhes do problema
3. Inclua logs de erro e informações do sistema

## 🙏 Agradecimentos

- [OpenAI Whisper](https://github.com/openai/whisper) - Transcrição de áudio
- [Google Gemini](https://ai.google.dev/) - Geração de resumos
- [yt-dlp](https://github.com/yt-dlp/yt-dlp) - Download de vídeos
- [FastAPI](https://fastapi.tiangolo.com/) - Framework web

## 📈 Roadmap

- [ ] Suporte a múltiplos idiomas
- [ ] Cache de transcrições
- [ ] Interface para upload de arquivos locais
- [ ] API REST completa
- [ ] Suporte a playlists
- [ ] Integração com outras plataformas de vídeo

---

⭐ Se este projeto foi útil, considere dar uma estrela!
