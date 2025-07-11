"""
Testes unitários para o Resumidor de Vídeos do YouTube
"""

import os
import tempfile
from unittest.mock import Mock, patch

import pytest
from fastapi.testclient import TestClient

# Importar a aplicação
from main import app


@pytest.fixture
def client():
    """Cliente de teste FastAPI"""
    return TestClient(app)


@pytest.fixture
def mock_env_vars():
    """Mock das variáveis de ambiente"""
    with patch.dict(os.environ, {"GEMINI_API_KEY": "test_key"}):
        yield


class TestMainEndpoints:
    """Testes para os endpoints principais"""

    def test_home_endpoint(self, client):
        """Testa se a página inicial carrega corretamente"""
        response = client.get("/")
        assert response.status_code == 200
        assert "Resumo Inteligente de Vídeo do YouTube" in response.text
        assert "text/html" in response.headers["content-type"]

    def test_analisar_video_missing_url(self, client):
        """Testa erro quando URL não é fornecida"""
        response = client.get("/analisar_video")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "error"
        assert "URL não foi enviado" in data["msg"]

    def test_analisar_video_invalid_url(self, client):
        """Testa erro quando URL inválida é fornecida"""
        response = client.get("/analisar_video?url=https://invalid-site.com/video")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "error"
        assert "Somente URLS do Youtube são aceitos" in data["msg"]

    @patch("main.is_youtube_url")
    @patch("main.yt_dlp.YoutubeDL")
    @patch("main.whisper.load_model")
    @patch("main.enviar_prompt_gemini")
    def test_analisar_video_success(
        self,
        mock_gemini,
        mock_whisper,
        mock_ytdl,
        mock_is_youtube,
        client,
        mock_env_vars,
    ):
        """Testa processamento bem-sucedido de vídeo"""
        # Configurar mocks
        mock_is_youtube.return_value = True

        mock_ytdl_instance = Mock()
        mock_ytdl.return_value.__enter__.return_value = mock_ytdl_instance

        mock_model = Mock()
        mock_model.transcribe.return_value = {"text": "Texto transcrito"}
        mock_whisper.return_value = mock_model

        mock_gemini.return_value = "<html><body>Resumo HTML</body></html>"

        # Fazer requisição
        response = client.get("/analisar_video?url=https://youtube.com/watch?v=test")

        # Verificar que os mocks foram chamados
        assert mock_is_youtube.called
        assert mock_ytdl.called
        assert mock_whisper.called
        assert mock_gemini.called


class TestUtilityFunctions:
    """Testes para funções utilitárias"""

    def test_is_youtube_url_valid_urls(self):
        """Testa validação de URLs válidas do YouTube"""
        from main import is_youtube_url

        valid_urls = [
            "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
            "https://youtube.com/watch?v=dQw4w9WgXcQ",
            "http://www.youtube.com/watch?v=dQw4w9WgXcQ",
            "https://youtu.be/dQw4w9WgXcQ",
            "http://youtu.be/dQw4w9WgXcQ",
        ]

        for url in valid_urls:
            assert is_youtube_url(url), f"URL deveria ser válida: {url}"

    def test_is_youtube_url_invalid_urls(self):
        """Testa validação de URLs inválidas"""
        from main import is_youtube_url

        invalid_urls = [
            "https://vimeo.com/123456",
            "https://www.google.com",
            "not_a_url",
            "",
            "ftp://youtube.com/video",
            "https://fake-youtube.com/watch?v=test",
        ]

        for url in invalid_urls:
            assert not is_youtube_url(url), f"URL deveria ser inválida: {url}"

    @patch("main.genai.GenerativeModel")
    def test_enviar_prompt_gemini_success(self, mock_model):
        """Testa envio bem-sucedido para Gemini"""
        from main import enviar_prompt_gemini

        # Configurar mock
        mock_instance = Mock()
        mock_instance.generate_content.return_value.text = "Resposta do Gemini"
        mock_model.return_value = mock_instance

        # Testar função
        result = enviar_prompt_gemini("Prompt de teste")

        assert result == "Resposta do Gemini"
        mock_model.assert_called_once_with("gemini-2.0-flash")
        mock_instance.generate_content.assert_called_once_with("Prompt de teste")

    @patch("main.genai.GenerativeModel")
    def test_enviar_prompt_gemini_error(self, mock_model):
        """Testa tratamento de erro no Gemini"""
        from main import enviar_prompt_gemini

        # Configurar mock para lançar exceção
        mock_model.side_effect = Exception("Erro de API")

        # Testar função
        result = enviar_prompt_gemini("Prompt de teste")

        assert "Ocorreu um erro: Erro de API" in result


class TestIntegration:
    """Testes de integração"""

    @pytest.mark.integration
    @pytest.mark.slow
    def test_whisper_model_loading(self):
        """Testa se o modelo Whisper pode ser carregado"""
        import whisper

        # Testar carregamento do modelo tiny (mais rápido para testes)
        try:
            model = whisper.load_model("tiny")
            assert model is not None
            assert hasattr(model, "transcribe")
        except Exception as e:
            pytest.skip(f"Não foi possível carregar o modelo Whisper: {e}")

    @pytest.mark.integration
    def test_torch_cuda_detection(self):
        """Testa detecção de CUDA/GPU"""
        import torch

        # Verificar se torch funciona
        assert torch is not None

        # Verificar detecção de CUDA (pode ou não estar disponível)
        cuda_available = torch.cuda.is_available()
        assert isinstance(cuda_available, bool)


class TestFileOperations:
    """Testes para operações de arquivo"""

    def test_temp_file_creation(self):
        """Testa criação de arquivos temporários"""
        import uuid

        # Simular criação de nome único
        unique_id = str(uuid.uuid4())
        wav_path = f"video_{unique_id}.wav"
        html_path = f"resumo_video_{unique_id}.html"

        assert unique_id in wav_path
        assert unique_id in html_path
        assert wav_path != html_path

    def test_html_cleaning(self):
        """Testa limpeza de código HTML"""
        # Simular limpeza de markdown do HTML retornado pelo Gemini
        test_cases = [
            ("```html\n<html>content</html>\n```", "<html>content</html>"),
            ("```html\n<html>content</html>", "<html>content</html>"),
            ("<html>content</html>\n```", "<html>content</html>"),
            ("<html>content</html>", "<html>content</html>"),
        ]

        for input_html, expected in test_cases:
            # Simular a lógica de limpeza do código
            result = input_html.strip()
            if result.startswith("```html"):
                result = result[7:]
            if result.endswith("```"):
                result = result[:-3]
            result = result.strip()

            assert result == expected


if __name__ == "__main__":
    pytest.main([__file__])
