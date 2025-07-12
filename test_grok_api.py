#!/usr/bin/env python3
"""
Teste Rápido da API Grok
"""

import requests
import json

# Configurações da API
XAI_API_KEY = "xai-ALAspSpCmyKga42PSR4xQNmHjuj68ux2lDHUC8RS9SBPTNrTBe4ZSAZDE42PhI96tJqq7hjRstilmGWp"
XAI_API_URL = "https://api.x.ai/v1/chat/completions"

def test_grok_connection():
    """Testa a conexão básica com a API Grok"""
    
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {XAI_API_KEY}"
    }
    
    # Teste simples
    test_messages = [
        {"role": "system", "content": "Você é um assistente útil."},
        {"role": "user", "content": "Olá! Pode me dizer 'Olá, API Grok funcionando!' se estiver tudo ok?"}
    ]
    
    payload = {
        "messages": test_messages,
        "model": "grok-4",
        "stream": False
    }
    
    print("🔍 Testando conexão com Grok API...")
    print(f"URL: {XAI_API_URL}")
    print(f"API Key: {XAI_API_KEY[:20]}...")
    print("-" * 50)
    
    try:
        response = requests.post(
            XAI_API_URL,
            headers=headers,
            json=payload,
            timeout=15
        )
        
        print(f"📡 Status Code: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            content = result.get("choices", [{}])[0].get("message", {}).get("content", "")
            print("✅ Conexão estabelecida com sucesso!")
            print(f"🤖 Resposta do Grok: {content}")
            return True
        else:
            print(f"❌ Erro na API: {response.status_code}")
            print(f"Resposta: {response.text}")
            return False
            
    except requests.exceptions.Timeout:
        print("⏰ Timeout - API não respondeu em tempo hábil")
        return False
    except requests.exceptions.ConnectionError:
        print("🔌 Erro de conexão - Verifique sua internet")
        return False
    except Exception as e:
        print(f"❌ Erro inesperado: {e}")
        return False

def test_grok_analysis():
    """Testa análise de dados com Grok"""
    
    if not test_grok_connection():
        return
    
    print("\n" + "="*50)
    print("🧠 Testando análise de dados...")
    print("="*50)
    
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {XAI_API_KEY}"
    }
    
    # Dados de exemplo
    data_summary = """
    Dados de 200 cidades brasileiras:
    - São Paulo: PIB R$ 500 bi, População 12M, Desemprego 8.2%
    - Rio de Janeiro: PIB R$ 300 bi, População 6.7M, Desemprego 9.1%
    - Belo Horizonte: PIB R$ 200 bi, População 2.5M, Desemprego 7.5%
    """
    
    system_prompt = """Você é um especialista em análise de dados brasileiro.
    Analise os dados fornecidos e responda de forma clara e objetiva.
    Use formatação markdown quando apropriado."""
    
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": f"Analise estes dados e me diga: qual cidade tem o maior PIB e por que isso é importante para negócios?\n\n{data_summary}"}
    ]
    
    payload = {
        "messages": messages,
        "model": "grok-4",
        "stream": False
    }
    
    try:
        response = requests.post(
            XAI_API_URL,
            headers=headers,
            json=payload,
            timeout=30
        )
        
        if response.status_code == 200:
            result = response.json()
            content = result.get("choices", [{}])[0].get("message", {}).get("content", "")
            print("✅ Análise concluída!")
            print("\n📊 Resposta do Grok:")
            print("-" * 40)
            print(content)
            print("-" * 40)
        else:
            print(f"❌ Erro na análise: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Erro na análise: {e}")

if __name__ == "__main__":
    print("🚀 TESTE RÁPIDO DA API GROK")
    print("=" * 50)
    
    # Teste básico
    success = test_grok_connection()
    
    if success:
        # Teste de análise
        test_grok_analysis()
    
    print("\n" + "="*50)
    print("🏁 Teste concluído!")
    print("="*50) 