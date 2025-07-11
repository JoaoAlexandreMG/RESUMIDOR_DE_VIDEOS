# API Documentation

## Endpoints

### GET /

**Descrição**: PáAtualmente não há rate limiting implementado, mas recomenda-se:

- Máximo 10 requisições por minuto por IP
- Timeout de 10 minutos por processamento

## URLs Aceitas

**Formatos do YouTube aceitos**:

- `https://www.youtube.com/watch?v=VIDEO_ID`
- `https://youtube.com/watch?v=VIDEO_ID`
- `https://youtu.be/VIDEO_ID`
- `http://www.youtube.com/watch?v=VIDEO_ID` (redirecionado para HTTPS)pal da aplicação com interface web.

**Parâmetros**: Nenhum

**Resposta**: HTML da interface principal

**Exemplo**:

```http
GET http://localhost:8000/
```

### GET /analisar_video

**Descrição**: Processa um vídeo do YouTube e retorna resumo em HTML.

**Parâmetros**:

- `url` (string, obrigatório): URL do vídeo do YouTube
- `pergunta` (string, opcional): Pergunta específica sobre o vídeo

**Resposta**:

- **Sucesso**: Arquivo HTML para download
- **Erro**: JSON com detalhes do erro

**Exemplos**:

**Resumo simples**:

```http
GET http://localhost:8000/analisar_video?url=https://youtube.com/watch?v=VIDEO_ID
```

**Pergunta específica**:

```http
GET http://localhost:8000/analisar_video?url=https://youtube.com/watch?v=VIDEO_ID&pergunta=Quais são os pontos principais do vídeo?
```

**Respostas de erro**:

```json
{
  "status": "error",
  "msg": "URL não foi enviado!"
}
```

```json
{
  "status": "error", 
  "msg": "Somente URLS do Youtube são aceitos!"
}
```

## Códigos de Status

- **200**: Sucesso (retorna HTML ou JSON de erro)
- **500**: Erro interno do servidor

## Rate Limiting

Atualmente não há rate limiting implementado, mas recomenda-se:

- Máximo 10 requisições por minuto por IP
- Timeout de 10 minutos por processamento

## Formatos Aceitos

**URLs do YouTube aceitas**:

- `https://www.youtube.com/watch?v=VIDEO_ID`
- `https://youtube.com/watch?v=VIDEO_ID`
- `https://youtu.be/VIDEO_ID`
- `http://www.youtube.com/watch?v=VIDEO_ID` (redirecionado para HTTPS)

## Limitações

- Vídeos muito longos (>2h) podem causar timeout
- Vídeos privados ou com restrição regional não funcionam
- Qualidade da transcrição depende da qualidade do áudio
- Apenas vídeos do YouTube são suportados
