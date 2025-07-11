# Histórico de Mudanças

Todas as mudanças notáveis neste projeto serão documentadas neste arquivo.

O formato é baseado em [Keep a Changelog](https://keepachangelog.com/pt-BR/1.0.0/),
e este projeto adere ao [Versionamento Semântico](https://semver.org/lang/pt-BR/).

## [1.0.0] - 2025-07-11

### Adicionado

- ✨ Funcionalidade principal de análise de vídeos do YouTube
- 🎙️ Transcrição automática usando OpenAI Whisper
- 🤖 Geração de resumos inteligentes com Google Gemini 2.0 Flash
- 🎨 Interface web moderna e responsiva
- 📱 Suporte a dispositivos móveis
- ⚡ Detecção automática de GPU para acelerar transcrição
- 📄 Export de resumos em formato HTML estilizado
- 🔧 API REST com FastAPI
- 📊 Barra de progresso para feedback visual
- 🛡️ Validação de URLs do YouTube
- 🧹 Limpeza automática de arquivos temporários
- 🎛️ Opções personalizáveis para modelos Whisper

### Funcionalidades Técnicas

- Integração com yt-dlp para download de áudio
- Suporte a múltiplos formatos de áudio
- Processamento assíncrono com FastAPI
- Interface HTML/CSS/JavaScript embarcada
- Gerenciamento de arquivos temporários únicos
- Tratamento de erros robusto

### Dependências

- FastAPI para o servidor web
- OpenAI Whisper para transcrição
- Google Generative AI para resumos
- yt-dlp para download de vídeos
- PyTorch para aceleração GPU
- python-dotenv para configuração
- uvicorn como servidor ASGI

### Recursos de Interface

- Design moderno com gradientes e sombras
- Animações CSS suaves
- Ícones visuais atraentes
- Feedback visual durante processamento
- Download automático de resultados
- Mensagens de erro informativas

### Próximas Versões Planejadas

- [ ] v1.1.0: Suporte a múltiplos idiomas
- [ ] v1.2.0: Cache de transcrições
- [ ] v1.3.0: Upload de arquivos locais
- [ ] v2.0.0: Interface completa de administração
