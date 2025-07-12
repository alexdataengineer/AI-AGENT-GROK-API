#!/usr/bin/env python3
"""
Script de teste para o Agente de Análise de Dados
"""

import sys
import os
from data_analysis_agent import DataAnalysisAgent

def test_agent():
    """
    Testa as funcionalidades principais do agente
    """
    print("🧪 Iniciando testes do agente...")
    
    try:
        # Inicializar agente
        print("1. Inicializando agente...")
        agent = DataAnalysisAgent()
        print("✅ Agente inicializado com sucesso!")
        
        # Testar visão geral dos dados
        print("\n2. Testando visão geral dos dados...")
        data_overview = agent.get_data_overview()
        print(f"✅ Dados carregados: {data_overview['total_records']} registros")
        
        # Testar processamento de perguntas
        test_questions = [
            "Quais são as 10 cidades com maior PIB?",
            "Analise a correlação entre população e PIB",
            "Compare as regiões do Brasil",
            "Busque informações sobre São Paulo"
        ]
        
        print("\n3. Testando processamento de perguntas...")
        for i, question in enumerate(test_questions, 1):
            print(f"\n   Teste {i}: {question}")
            result = agent.process_user_input(question)
            
            print(f"   ✅ Tipo: {result['decision_type']}")
            print(f"   ✅ Confiança: {result['confidence']:.2f}")
            print(f"   ✅ Qualidade: {result['quality_metrics']['overall_score']:.2f}")
            
            if result.get('needs_human_help'):
                print(f"   ⚠️  Precisa de ajuda humana: {result.get('help_reason', 'N/A')}")
            else:
                print(f"   ✅ Resposta gerada automaticamente")
        
        # Testar memória
        print("\n4. Testando sistema de memória...")
        memory_summary = agent.get_memory_summary()
        print(f"✅ Interações na memória: {memory_summary.get('total_interactions', 0)}")
        
        # Testar busca na memória
        print("\n5. Testando busca na memória...")
        memory_results = agent.search_memory("PIB")
        print(f"✅ Resultados encontrados: {len(memory_results)}")
        
        # Testar exportação de memória
        print("\n6. Testando exportação de memória...")
        success = agent.export_memory("test_memory.json")
        if success:
            print("✅ Memória exportada com sucesso!")
        else:
            print("❌ Erro ao exportar memória")
        
        # Limpar recursos
        print("\n7. Limpando recursos...")
        agent.close()
        print("✅ Recursos liberados!")
        
        print("\n🎉 Todos os testes passaram com sucesso!")
        print("\n📋 Resumo dos testes:")
        print("   ✅ Inicialização do agente")
        print("   ✅ Carregamento de dados")
        print("   ✅ Processamento de perguntas")
        print("   ✅ Sistema de memória")
        print("   ✅ Busca na memória")
        print("   ✅ Exportação de dados")
        print("   ✅ Limpeza de recursos")
        
        return True
        
    except Exception as e:
        print(f"❌ Erro durante os testes: {e}")
        return False

def test_grok_api():
    """
    Testa a integração com a API Grok
    """
    print("\n🌐 Testando integração com Grok API...")
    
    try:
        from grok_api import GrokAPI
        
        grok = GrokAPI()
        
        # Teste simples
        messages = [
            {"role": "system", "content": "Você é um assistente útil."},
            {"role": "user", "content": "Olá! Como você está?"}
        ]
        
        response = grok.chat_completion(messages)
        
        if "error" in response:
            print(f"❌ Erro na API Grok: {response['error']}")
            return False
        else:
            print("✅ Integração com Grok API funcionando!")
            return True
            
    except Exception as e:
        print(f"❌ Erro ao testar Grok API: {e}")
        return False

def test_data_manager():
    """
    Testa o gerenciador de dados
    """
    print("\n📊 Testando gerenciador de dados...")
    
    try:
        from data_manager import DataManager
        
        data_manager = DataManager()
        
        # Testar consultas básicas
        summary = data_manager.get_data_summary()
        print(f"✅ Resumo dos dados: {summary.get('total_registros', 0)} registros")
        
        # Testar busca
        search_results = data_manager.search_cities("São Paulo")
        print(f"✅ Busca por São Paulo: {len(search_results)} resultados")
        
        # Testar análise por região
        region_analysis = data_manager.analyze_by_region()
        print(f"✅ Análise por região: {len(region_analysis)} regiões")
        
        data_manager.close()
        print("✅ Gerenciador de dados funcionando!")
        return True
        
    except Exception as e:
        print(f"❌ Erro ao testar gerenciador de dados: {e}")
        return False

if __name__ == "__main__":
    print("🚀 Iniciando testes do Agente de Análise de Dados")
    print("=" * 50)
    
    # Executar testes
    tests = [
        ("Agente Principal", test_agent),
        ("Grok API", test_grok_api),
        ("Gerenciador de Dados", test_data_manager)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        print(f"\n🧪 Executando teste: {test_name}")
        print("-" * 30)
        
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ Erro no teste {test_name}: {e}")
            results.append((test_name, False))
    
    # Resumo final
    print("\n" + "=" * 50)
    print("📋 RESUMO DOS TESTES")
    print("=" * 50)
    
    passed = 0
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASSOU" if result else "❌ FALHOU"
        print(f"{test_name}: {status}")
        if result:
            passed += 1
    
    print(f"\n🎯 Resultado: {passed}/{total} testes passaram")
    
    if passed == total:
        print("🎉 Todos os testes passaram! O agente está funcionando corretamente.")
        sys.exit(0)
    else:
        print("⚠️  Alguns testes falharam. Verifique os erros acima.")
        sys.exit(1) 