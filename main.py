"""
App para baixar áudio de vídeos do YouTube, transcrever com Whisper e gerar resumo em HTML usando Gemini.
Interface moderna com customtkinter, barra de progresso e detecção automática de GPU.
"""

import uvicorn
from fastapi import FastAPI
from fastapi.responses import FileResponse, HTMLResponse

app = FastAPI()


@app.get("/analisar_video")
async def analisar_video(url: str = "", pergunta: str = ""):
    import os
    import re
    import threading
    import time
    import uuid

    import google.generativeai as genai
    import torch
    import whisper
    import yt_dlp
    from dotenv import load_dotenv

    # Carrega variáveis de ambiente e configura API do Gemini
    load_dotenv()
    API_KEY = os.getenv("GEMINI_API_KEY")
    genai.configure(api_key=API_KEY)

    def enviar_prompt_gemini(prompt_texto: str) -> str:
        """
        Envia um prompt de texto para o modelo Gemini e retorna a resposta.
        :param prompt_texto: Texto do prompt a ser enviado.
        :return: Resposta gerada pelo Gemini.
        """
        try:
            model = genai.GenerativeModel("gemini-2.0-flash")
            response = model.generate_content(prompt_texto)
            return response.text
        except Exception as e:
            return f"Ocorreu um erro: {e}"

    def is_youtube_url(url: str) -> bool:
        """
        Verifica se a string é uma URL válida do YouTube.
        :param url: URL a ser validada.
        :return: True se for do YouTube, False caso contrário.
        """
        pattern = r"^(https?://)?(www\.)?(youtube\.com|youtu\.be)/.+$"
        return re.match(pattern, url) is not None

    try:
        # Validação do campo
        if not url:
            return {"status": "error", "msg": "URL não foi enviado!"}
        if not is_youtube_url(url):
            return {"status": "error", "msg": "Somente URLS do Youtube são aceitos!"}
        # Gera nome de arquivo único para cada requisição
        unique_id = str(uuid.uuid4())
        wav_path = f"video_{unique_id}.wav"
        html_path = f"resumo_video_{unique_id}.html"
        # Opções do yt_dlp para salvar áudio temporário único
        ydl_opts = {
            "format": "bestaudio[ext=m4a]/bestaudio/best",
            "postprocessors": [
                {
                    "key": "FFmpegExtractAudio",
                    "preferredcodec": "wav",
                    "preferredquality": "192",
                }
            ],
            "outtmpl": f"video_{unique_id}.%(ext)s",
            "ffmpeg_location": "ffmpeg.exe",
            "noplaylist": True,
            "quiet": True,
            "no_warnings": True,
            "ignoreerrors": True,
            "nooverwrites": True,
            "writethumbnail": False,
            "writeinfojson": False,
            "writesubtitles": False,
            "writeautomaticsub": False,
            "skip_download": False,
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        # Detecta GPU e informa ao usuário
        device = "cuda" if torch.cuda.is_available() else "cpu"
        # Transcrição com Whisper
        model = whisper.load_model("tiny", device=device)
        result = model.transcribe(wav_path)
        # Prompt para Gemini: personalizado conforme pergunta do usuário
        if pergunta:
            prompt_base = (
                "Aqui está a transcrição de um vídeo do YouTube. Com base nela, responda à solicitação do usuário abaixo, gerando APENAS um código HTML completo, pronto para ser aberto diretamente em um navegador moderno. O HTML deve conter as tags <html>, <head>, <meta charset='utf-8'>, <title>, <body> e usar CSS embutido para visual bonito, responsivo e moderno. NÃO inclua explicações, comentários, markdown, mensagens extras ou qualquer texto fora do HTML.\n\n"
                "Solicitação do usuário: '" + pergunta + "'.\n\nTranscrição: "
            )
        else:
            prompt_base = (
                "Aqui está a transcrição de um vídeo do YouTube. Gere APENAS um código HTML completo, pronto para ser aberto diretamente em um navegador moderno, que resuma o conteúdo do vídeo. O HTML deve conter as tags <html>, <head>, <meta charset='utf-8'>, <title>, <body> e usar CSS embutido para visual bonito, responsivo e moderno. NÃO inclua explicações, comentários, markdown, mensagens extras ou qualquer texto fora do HTML.\n\n"
                "Transcrição: "
            )
        resumo_html = enviar_prompt_gemini(prompt_base + result["text"])
        # Remove possíveis blocos de markdown do início/fim
        if resumo_html.strip().startswith("```html"):
            resumo_html = resumo_html.strip()[7:]
        if resumo_html.strip().endswith("```"):
            resumo_html = resumo_html.strip()[:-3]
        # Salva o HTML gerado
        with open(html_path, "w", encoding="utf-8") as file:
            file.write(resumo_html.strip())

        # Exclui o arquivo .wav após a transcrição
        def remove_temp_files(paths):
            time.sleep(2)
            for path in paths:
                try:
                    if os.path.exists(path):
                        os.remove(path)
                except Exception as e:
                    print(f"Não foi possível remover {path}: {e}")

        threading.Thread(
            target=remove_temp_files, args=([wav_path, html_path],), daemon=True
        ).start()
        return FileResponse(
            html_path,
            media_type="text/html",
            filename="resumo_video.html",
        )
    except Exception as e:
        return {"status": "error", "msg": str(e)}


@app.get("/", response_class=HTMLResponse)
def home():
    return """
    <html>
    <head>
        <title>Resumo de Vídeo do YouTube</title>
        <meta charset='utf-8'>
        <meta name='viewport' content='width=device-width, initial-scale=1'>
        <link rel='icon' href='https://cdn-icons-png.flaticon.com/512/8089/8089662.png'>
        <style>
            body {
                min-height: 100vh;
                margin: 0;
                background: linear-gradient(120deg, #1e90ff 0%, #f4f6fa 100%);
                display: flex;
                align-items: center;
                justify-content: center;
                font-family: 'Segoe UI', Arial, sans-serif;
            }
            .box {
                background: #fff;
                padding: 40px 32px 32px 32px;
                border-radius: 18px;
                box-shadow: 0 8px 32px #0002, 0 1.5px 8px #1e90ff22;
                max-width: 420px;
                width: 100%;
                margin: 32px 0;
                display: flex;
                flex-direction: column;
                align-items: center;
                animation: fadein 1s;
            }
            @keyframes fadein { from { opacity: 0; transform: translateY(30px);} to { opacity: 1; transform: none; } }
            .logo {
                width: 64px;
                height: 64px;
                margin-bottom: 12px;
                filter: drop-shadow(0 2px 8px #1e90ff33);
            }
            h2 {
                color: #1e90ff;
                margin-bottom: 8px;
                font-size: 2rem;
                letter-spacing: 0.5px;
            }
            p.desc {
                color: #444b;
                font-size: 1.08rem;
                margin-bottom: 18px;
            }
            input, button {
                padding: 12px;
                margin: 10px 0 0 0;
                width: 100%;
                min-width: 0;
                max-width: 100%;
                box-sizing: border-box;
                border-radius: 8px;
                border: 1px solid #dbeafe;
                font-size: 1.08rem;
                transition: border 0.2s;
            }
            input:focus {
                outline: none;
                border: 1.5px solid #1e90ff;
            }
            button {
                background: linear-gradient(90deg, #1e90ff 60%, #156dc1 100%);
                color: #fff;
                border: none;
                font-weight: 600;
                margin-top: 18px;
                box-shadow: 0 2px 8px #1e90ff22;
                cursor: pointer;
                letter-spacing: 0.5px;
                font-size: 1.13rem;
            }
            button:hover {
                background: linear-gradient(90deg, #156dc1 60%, #1e90ff 100%);
            }
            #loading {
                margin-top: 24px;
            }
            .credit {
                margin-top: 32px;
                color: #888b;
                font-size: 0.98rem;
            }
            @media (max-width: 600px) {
                .box { padding: 24px 6vw; }
                h2 { font-size: 1.3rem; }
            }
        </style>
    </head>
    <body>
        <div class="box">
            <img src="https://cdn-icons-png.flaticon.com/512/8089/8089662.png" class="logo" alt="logo">
            <h2>Resumo Inteligente de Vídeo do YouTube</h2>
            <p class="desc">Cole o link de um vídeo do YouTube e peça um resumo ou uma análise personalizada. O resultado será entregue em um HTML bonito e pronto para navegador.</p>
            <form id="form">
                <input type="text" id="url" placeholder="Cole o link do YouTube" required><br>
                <input type="text" id="pergunta" placeholder="O que você deseja saber? (opcional)"><br>
                <button type="submit">Analisar</button>
            </form>
            <div id="loading" style="display:none;">
                <p>Processando vídeo, isso pode levar alguns minutos...</p>
                <div style="margin:20px auto;width:40px;height:40px;">
                    <svg viewBox="0 0 50 50"><circle cx="25" cy="25" r="20" fill="none" stroke="#1e90ff" stroke-width="5" stroke-linecap="round" stroke-dasharray="31.4 31.4" transform="rotate(-90 25 25)"><animateTransform attributeName="transform" type="rotate" from="0 25 25" to="360 25 25" dur="1s" repeatCount="indefinite"/></circle></svg>
                </div>
            </div>
            <div class="credit">Desenvolvido por John</div>
        </div>
        <script>
        const form = document.getElementById('form');
        const loading = document.getElementById('loading');
        form.onsubmit = async (e) => {
            e.preventDefault();
            form.style.display = 'none';
            loading.style.display = 'block';
            const url = document.getElementById('url').value;
            const pergunta = document.getElementById('pergunta').value;
            try {
                const params = new URLSearchParams({ url, pergunta });
                const response = await fetch('/analisar_video?' + params, { method: 'GET' });
                if (response.ok) {
                    const blob = await response.blob();
                    const a = document.createElement('a');
                    a.href = window.URL.createObjectURL(blob);
                    a.download = 'resumo_video.html';
                    a.click();
                    loading.innerHTML = '<b>Download iniciado!</b><br><button id="novo">Analisar outro vídeo</button>';
                    document.getElementById('novo').onclick = () => window.location.reload();
                } else {
                    const err = await response.json();
                    loading.innerHTML = '<span style="color:red">Erro: ' + (err.msg || 'Falha ao processar') + '</span><br><button id="novo">Tentar outro vídeo</button>';
                    document.getElementById('novo').onclick = () => window.location.reload();
                }
            } catch (err) {
                loading.innerHTML = '<span style="color:red">Erro inesperado!</span>';
            }
        };
        </script>
    </body>
    </html>
    """


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
