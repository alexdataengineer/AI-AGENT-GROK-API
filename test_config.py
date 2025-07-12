#!/usr/bin/env python3
"""
Script de teste para verificar a configuração segura da API
"""

import os
from dotenv import load_dotenv

def test_configuration():
    """Testa se a configuração está segura e funcionando"""
    
    print("🔒 Testando Configuração Segura da API")
    print("=" * 50)
    
    # Teste 1: Verificar se .env existe
    if os.path.exists('.env'):
        print("✅ Arquivo .env encontrado")
    else:
        print("❌ Arquivo .env não encontrado")
        print("   Execute: cp .env.example .env")
        return False
    
    # Teste 2: Verificar se .env está no .gitignore
    if os.path.exists('.gitignore'):
        with open('.gitignore', 'r') as f:
            gitignore_content = f.read()
            if '.env' in gitignore_content:
                print("✅ .env está no .gitignore")
            else:
                print("❌ .env não está no .gitignore")
                return False
    else:
        print("❌ .gitignore não encontrado")
        return False
    
    # Teste 3: Verificar se .env.example existe
    if os.path.exists('.env.example'):
        print("✅ .env.example encontrado")
    else:
        print("❌ .env.example não encontrado")
        return False
    
    # Teste 4: Testar carregamento da configuração
    try:
        load_dotenv()
        api_key = os.getenv('XAI_API_KEY')
        
        if api_key and api_key != 'your_xai_api_key_here':
            print("✅ API key configurada corretamente")
            print(f"   Key: {api_key[:10]}...{api_key[-10:]}")
        else:
            print("❌ API key não configurada ou está no valor padrão")
            print("   Edite o arquivo .env com sua API key real")
            return False
            
    except Exception as e:
        print(f"❌ Erro ao carregar configuração: {e}")
        return False
    
    # Teste 5: Verificar se não há API keys hardcoded
    try:
        with open('config.py', 'r') as f:
            config_content = f.read()
            if 'xai-' in config_content and 'ALAspSpCmyKga42PSR4xQNmHjuj68ux2lDHUC8RS9SBPTNrTBe4ZSAZDE42PhI96tJqq7hjRstilmGWp' in config_content:
                print("❌ API key ainda está hardcoded no config.py")
                return False
            else:
                print("✅ API key removida do código fonte")
    except Exception as e:
        print(f"❌ Erro ao verificar config.py: {e}")
        return False
    
    print("\n🎉 Todos os testes passaram!")
    print("✅ Sua configuração está segura para subir no GitHub")
    return True

def test_api_connection():
    """Testa a conexão com a API"""
    
    print("\n🔗 Testando Conexão com a API")
    print("=" * 50)
    
    try:
        from grok_api import GrokAPI
        
        api = GrokAPI()
        response = api.chat_completion([
            {"role": "user", "content": "Teste de conexão"}
        ])
        
        if "error" not in response:
            print("✅ Conexão com Grok API estabelecida")
            return True
        else:
            print(f"❌ Erro na API: {response['error']}")
            return False
            
    except Exception as e:
        print(f"❌ Erro ao testar API: {e}")
        return False

if __name__ == "__main__":
    print("🚀 Teste de Configuração Segura")
    print("=" * 50)
    
    config_ok = test_configuration()
    
    if config_ok:
        api_ok = test_api_connection()
        
        if api_ok:
            print("\n🎉 Sistema pronto para uso!")
            print("✅ Configuração segura")
            print("✅ API funcionando")
            print("✅ Pronto para subir no GitHub")
        else:
            print("\n⚠️ Configuração segura, mas API com problemas")
            print("   Verifique sua conexão com a internet")
    else:
        print("\n❌ Problemas na configuração encontrados")
        print("   Siga as instruções acima para corrigir") 