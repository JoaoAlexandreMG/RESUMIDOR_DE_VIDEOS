# Guia de Contribuição

Obrigado pelo seu interesse em contribuir com o Resumidor de Vídeos do YouTube! Este documento fornece diretrizes para contribuir com o projeto.

## 🤝 Como Contribuir

### Reportar Bugs

1. **Verifique se o bug já foi reportado** nos [issues existentes](https://github.com/seu-usuario/resumidor-videos-youtube/issues)
2. **Crie um novo issue** se o bug não foi reportado ainda
3. **Use o template de bug report** e inclua:
   - Descrição clara do problema
   - Passos para reproduzir
   - Comportamento esperado vs atual
   - Screenshots (se aplicável)
   - Informações do sistema (OS, Python version, etc.)

### Sugerir Melhorias

1. **Verifique os issues existentes** para evitar duplicatas
2. **Crie um novo issue** com label "enhancement"
3. **Descreva a melhoria** detalhadamente:
   - Problema que resolve
   - Solução proposta
   - Alternativas consideradas
   - Impacto nos usuários

### Desenvolver Features

1. **Fork o repositório**
2. **Crie uma branch** para sua feature:
   ```bash
   git checkout -b feature/nome-da-feature
   ```
3. **Faça suas alterações** seguindo as convenções do projeto
4. **Teste suas alterações** completamente
5. **Commit suas mudanças** com mensagens descritivas
6. **Push para sua branch**:
   ```bash
   git push origin feature/nome-da-feature
   ```
7. **Abra um Pull Request**

## 📝 Convenções de Código

### Python

- **PEP 8**: Siga o guia de estilo Python
- **Type hints**: Use type hints sempre que possível
- **Docstrings**: Documente funções e classes
- **Nomes descritivos**: Use nomes de variáveis e funções claros

### Commits

Use o padrão de [Conventional Commits](https://www.conventionalcommits.org/):

```
tipo(escopo): descrição

[corpo opcional]

[rodapé opcional]
```

**Tipos:**
- `feat`: nova funcionalidade
- `fix`: correção de bug
- `docs`: documentação
- `style`: formatação/estilo
- `refactor`: refatoração de código
- `test`: testes
- `chore`: tarefas de manutenção

**Exemplos:**
```bash
feat(whisper): adicionar suporte ao modelo large
fix(api): corrigir erro de timeout em vídeos longos
docs(readme): atualizar instruções de instalação
```

## 🧪 Testes

### Executar Testes

```bash
# Instalar dependências de teste
pip install pytest pytest-asyncio

# Executar todos os testes
pytest

# Executar com cobertura
pytest --cov=main
```

### Escrever Testes

- **Teste todas as funções públicas**
- **Use fixtures para dados de teste**
- **Teste casos de erro**
- **Mantenha testes independentes**

## 📁 Estrutura do Projeto

```text
resumidor-videos-youtube/
├── main.py              # Aplicação principal
├── tests/              # Testes unitários
│   ├── test_main.py
│   └── test_utils.py
├── docs/               # Documentação adicional
├── requirements.txt    # Dependências
├── requirements-dev.txt # Dependências de desenvolvimento
└── .github/           # Templates e workflows
    ├── ISSUE_TEMPLATE/
    └── workflows/
```

## 🚀 Ambiente de Desenvolvimento

### Configuração Inicial

1. **Clone e acesse o diretório**:
   ```bash
   git clone https://github.com/seu-usuario/resumidor-videos-youtube.git
   cd resumidor-videos-youtube
   ```

2. **Crie um ambiente virtual**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   venv\Scripts\activate     # Windows
   ```

3. **Instale dependências**:
   ```bash
   pip install -r requirements.txt
   pip install -r requirements-dev.txt
   ```

4. **Configure variáveis de ambiente**:
   ```bash
   cp .env.example .env
   # Edite .env com suas configurações
   ```

### Ferramentas Recomendadas

- **IDE**: VS Code com extensões Python
- **Linting**: flake8, black
- **Type checking**: mypy
- **Testes**: pytest

## 🎯 Áreas que Precisam de Contribuição

### Prioridade Alta
- [ ] Melhorar tratamento de erros
- [ ] Adicionar testes unitários
- [ ] Otimizar performance
- [ ] Documentar API

### Prioridade Média
- [ ] Suporte a múltiplos idiomas
- [ ] Interface de administração
- [ ] Cache de resultados
- [ ] Docker container

### Prioridade Baixa
- [ ] Temas personalizáveis
- [ ] Estatísticas de uso
- [ ] Integração com serviços externos

## 🔍 Processo de Review

### Para Maintainers

1. **Verificar compatibilidade** com objetivos do projeto
2. **Revisar código** quanto a qualidade e padrões
3. **Testar funcionalidade** localmente
4. **Verificar documentação** adequada
5. **Confirmar testes** passando

### Para Contribuidores

- **Responda a feedback** rapidamente
- **Faça alterações** solicitadas
- **Mantenha PR atualizado** com main branch
- **Seja paciente** durante o processo

## 📞 Comunicação

### Channels

- **Issues**: Para bugs e features
- **Discussions**: Para perguntas gerais
- **Email**: contato@projeto.com (para questões sensíveis)

### Expectativas

- **Seja respeitoso** e construtivo
- **Use linguagem clara** e profissional
- **Forneça contexto** suficiente
- **Seja paciente** com respostas

## 🏆 Reconhecimento

Contribuidores serão reconhecidos:

- **README**: Lista de contribuidores
- **CHANGELOG**: Créditos em releases
- **Social**: Mention em redes sociais

## 📚 Recursos Úteis

- [Guia Git](https://git-scm.com/doc)
- [PEP 8 Style Guide](https://pep8.org/)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Pytest Documentation](https://docs.pytest.org/)

---

Obrigado por contribuir! 🎉
