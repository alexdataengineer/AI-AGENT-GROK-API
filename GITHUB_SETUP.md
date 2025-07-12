# 🚀 Configuração para GitHub

## ⚠️ IMPORTANTE: Proteção da API Key

Este projeto está configurado para proteger sua API key da xAI. **NUNCA** commite arquivos `.env` com suas credenciais reais!

## 📋 Passos para Configuração

### 1. Clone o Repositório
```bash
git clone <seu-repositorio>
cd AI-AGENT-GROK-API
```

### 2. Configure a API Key
```bash
# Copie o arquivo de exemplo
cp .env.example .env

# Edite o arquivo .env com sua API key real
nano .env  # ou use seu editor preferido
```

### 3. Adicione sua API Key no .env
```bash
# Grok API Configuration
XAI_API_KEY=sua_api_key_real_aqui
XAI_API_URL=https://api.x.ai/v1/chat/completions
```

### 4. Obtenha sua API Key
- Acesse: https://console.x.ai/
- Crie uma conta ou faça login
- Gere uma nova API key
- Copie a key para o arquivo `.env`

### 5. Teste a Configuração
```bash
python3 test_config.py
```

## 🔒 Segurança Implementada

### ✅ Proteções Ativas
- `.env` no `.gitignore` (não será commitado)
- API key removida do código fonte
- Validação de configuração no startup
- Template `.env.example` sem credenciais reais

### ✅ Verificações Automáticas
- Teste de configuração: `python3 test_config.py`
- Validação de API key no `config.py`
- Fallback local quando API falha

## 🚨 O que NÃO fazer

### ❌ NUNCA faça isso:
```bash
# NÃO commite o arquivo .env
git add .env
git commit -m "add api key"  # ❌ PERIGOSO!

# NÃO adicione a API key diretamente no código
XAI_API_KEY = "sua_key_aqui"  # ❌ PERIGOSO!
```

### ✅ SEMPRE faça isso:
```bash
# ✅ Use o arquivo .env
XAI_API_KEY = os.getenv('XAI_API_KEY')

# ✅ Mantenha .env no .gitignore
echo ".env" >> .gitignore

# ✅ Use .env.example como template
cp .env.example .env
```

## 🧪 Testes de Segurança

### Teste 1: Verificar se .env está protegido
```bash
git status
# O arquivo .env NÃO deve aparecer na lista
```

### Teste 2: Verificar configuração
```bash
python3 test_config.py
# Deve mostrar: ✅ Configuração segura
```

### Teste 3: Testar API
```bash
python3 test_grok_api.py
# Deve conectar com sucesso
```

## 📁 Estrutura de Arquivos Segura

```
AI-AGENT-GROK-API/
├── .env                 # ✅ Sua API key (não commitado)
├── .env.example         # ✅ Template sem credenciais
├── .gitignore          # ✅ Protege .env
├── config.py           # ✅ Carrega de variáveis de ambiente
├── test_config.py      # ✅ Testa segurança
└── README.md           # ✅ Instruções de configuração
```

## 🔧 Troubleshooting

### Erro: "XAI_API_KEY não encontrada"
```bash
# Solução:
cp .env.example .env
# Edite o arquivo .env com sua API key real
```

### Erro: "API não responde"
```bash
# Verifique:
1. Sua API key está correta?
2. Tem conexão com a internet?
3. A API da xAI está funcionando?
```

### Erro: "Arquivo .env não encontrado"
```bash
# Solução:
cp .env.example .env
nano .env  # Adicione sua API key
```

## 🎯 Próximos Passos

1. ✅ Configure sua API key no `.env`
2. ✅ Teste com `python3 test_config.py`
3. ✅ Execute o app: `python3 -m streamlit run agents/english/english_streamlit_app.py`
4. ✅ Faça commit das mudanças (SEM o .env)
5. ✅ Push para o GitHub

## 📞 Suporte

Se tiver problemas:
1. Verifique se seguiu todos os passos
2. Execute `python3 test_config.py`
3. Consulte o README.md principal
4. Abra uma issue no GitHub

---

**⚠️ LEMBRE-SE**: Nunca commite arquivos `.env` com suas API keys reais! 