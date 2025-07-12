# 🤖 Intelligent Data Analysis Agent with Grok API

Um agente inteligente de análise de dados que utiliza a API Grok da xAI para fornecer insights detalhados sobre dados de cidades brasileiras.

## 🚀 Características

- **Análise Inteligente**: Utiliza Grok API para insights avançados
- **Interface Web**: Streamlit app com visualizações interativas
- **Sistema de Memória**: Mantém histórico de conversas
- **Fallback Local**: Respostas locais quando API não está disponível
- **Múltiplos Idiomas**: Versões em português e inglês
- **Segurança**: API keys protegidas com variáveis de ambiente

## 📋 Pré-requisitos

- Python 3.8+
- Conta na xAI (https://console.x.ai/) para obter API key

## ⚙️ Configuração

### 1. Clone o repositório
```bash
git clone <seu-repositorio>
cd AI-AGENT-GROK-API
```

### 2. Instale as dependências
```bash
pip install -r requirements.txt
```

### 3. Configure a API Key

**IMPORTANTE**: Nunca commite sua API key no GitHub!

1. Copie o arquivo de exemplo:
```bash
cp .env.example .env
```

2. Edite o arquivo `.env` e adicione sua API key:
```bash
# Grok API Configuration
XAI_API_KEY=sua_api_key_aqui
XAI_API_URL=https://api.x.ai/v1/chat/completions
```

3. Obtenha sua API key em: https://console.x.ai/

## 🎯 Como Usar

### Interface Web (Recomendado)
```bash
# Versão em Português
python3 -m streamlit run agents/portuguese/portuguese_streamlit_app.py --server.port 8501

# Versão em Inglês
python3 -m streamlit run agents/english/english_streamlit_app.py --server.port 8502
```

### Linha de Comando
```bash
# Agente principal
python3 main.py

# Teste da API
python3 test_grok_api.py
```

## 📊 Funcionalidades

### Interface Web
- **Chat Interativo**: Faça perguntas sobre as cidades
- **Visualizações**: Gráficos e tabelas dos dados
- **Histórico**: Memória das conversas anteriores
- **Análises Comparativas**: Compare cidades e regiões

### Análises Disponíveis
- População e densidade demográfica
- PIB total e per capita
- Taxa de desemprego
- Índice de educação
- Comparações regionais
- Rankings e tendências

## 🔧 Estrutura do Projeto

```
AI-AGENT-GROK-API/
├── agents/
│   ├── portuguese/     # Versão em português
│   └── english/        # Versão em inglês
├── data/               # Dados das cidades
├── .env               # Configurações (não commitar!)
├── .env.example       # Template de configuração
├── config.py          # Configurações do sistema
├── grok_api.py        # Integração com Grok API
├── data_manager.py    # Gerenciamento de dados
├── memory_manager.py  # Sistema de memória
├── decision_engine.py # Motor de decisão
└── requirements.txt   # Dependências
```

## 🛡️ Segurança

- ✅ API keys protegidas em `.env`
- ✅ `.env` no `.gitignore`
- ✅ Validação de configuração
- ✅ Fallback local quando API falha

## 🔍 Exemplos de Perguntas

- "Como está São Paulo em comparação com outras cidades?"
- "Quais são as 5 cidades com maior PIB per capita?"
- "Como está o desemprego no Nordeste?"
- "Fortaleza é uma boa cidade para viver?"
- "Compare Brasília com Curitiba"

## 🚨 Troubleshooting

### Erro: "XAI_API_KEY não encontrada"
```bash
# Verifique se o arquivo .env existe
ls -la .env

# Crie o arquivo se não existir
cp .env.example .env
# Edite o arquivo .env com sua API key
```

### API não responde
- O sistema tem fallback local
- Verifique sua conexão com a internet
- Confirme se a API key está correta

### Porta já em uso
```bash
# Use uma porta diferente
python3 -m streamlit run agents/portuguese/portuguese_streamlit_app.py --server.port 8503
```

## 📈 Melhorias Futuras

- [ ] Suporte a mais idiomas
- [ ] Análises preditivas
- [ ] Exportação de relatórios
- [ ] Integração com mais APIs
- [ ] Dashboard administrativo

## 🤝 Contribuição

1. Fork o projeto
2. Crie uma branch para sua feature
3. Commit suas mudanças
4. Push para a branch
5. Abra um Pull Request

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo LICENSE para detalhes.

## 🔗 Links Úteis

- [xAI Console](https://console.x.ai/)
- [Streamlit Documentation](https://docs.streamlit.io/)
- [DuckDB Documentation](https://duckdb.org/docs/)

---

**⚠️ IMPORTANTE**: Nunca commite arquivos `.env` com suas API keys no GitHub!