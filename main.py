#!/usr/bin/env python3
"""
Agente de Análise de Dados com Grok API
========================================

Este agente possui:
✅ Memória persistente
✅ Loop de decisão inteligente
✅ Interação com múltiplas fontes (DuckDB + Grok API)
✅ Sistema human-in-the-loop
"""

import sys
import os
from data_analysis_agent import DataAnalysisAgent

def main():
    """
    Função principal para executar o agente
    """
    print("🚀 Iniciando Agente de Análise de Dados...")
    
    try:
        # Inicializar o agente
        agent = DataAnalysisAgent()
        
        # Mostrar visão geral dos dados
        data_overview = agent.get_data_overview()
        print(f"\n📊 Visão Geral dos Dados:")
        print(f"   • Total de registros: {data_overview['total_records']}")
        print(f"   • Cidades únicas: {data_overview['total_cities']}")
        print(f"   • Estados: {data_overview['total_states']}")
        print(f"   • Regiões: {data_overview['total_regions']}")
        print(f"   • População média: {data_overview['avg_population']:,.0f}")
        print(f"   • PIB per capita médio: R$ {data_overview['avg_gdp_per_capita']:,.2f}")
        
        print(f"\n💡 Exemplos de perguntas que você pode fazer:")
        print(f"   • 'Quais são as 10 cidades com maior PIB?'")
        print(f"   • 'Analise a correlação entre população e PIB'")
        print(f"   • 'Compare as regiões do Brasil'")
        print(f"   • 'Busque informações sobre São Paulo'")
        print(f"   • 'Gere insights sobre oportunidades de negócio'")
        print(f"   • 'Lembre-se da última análise que fizemos'")
        
        print(f"\n🔧 Comandos especiais:")
        print(f"   • 'memoria' - Ver resumo da memória")
        print(f"   • 'limpar' - Limpar memória")
        print(f"   • 'exportar' - Exportar memória")
        print(f"   • 'sair' - Encerrar programa")
        
        # Loop principal de interação
        while True:
            try:
                user_input = input(f"\n🤖 Digite sua pergunta: ").strip()
                
                if not user_input:
                    continue
                
                # Comandos especiais
                if user_input.lower() == 'sair':
                    print("👋 Encerrando agente...")
                    break
                
                elif user_input.lower() == 'memoria':
                    memory_summary = agent.get_memory_summary()
                    print(f"\n🧠 Resumo da Memória:")
                    print(f"   • Total de interações: {memory_summary.get('total_interactions', 0)}")
                    if memory_summary.get('total_interactions', 0) > 0:
                        print(f"   • Confiança média: {memory_summary.get('average_confidence', 0):.2f}")
                        print(f"   • Confiança mínima: {memory_summary.get('min_confidence', 0):.2f}")
                        print(f"   • Confiança máxima: {memory_summary.get('max_confidence', 0):.2f}")
                    continue
                
                elif user_input.lower() == 'limpar':
                    agent.clear_memory()
                    continue
                
                elif user_input.lower() == 'exportar':
                    success = agent.export_memory("memoria_agente.json")
                    if success:
                        print("✅ Memória exportada para 'memoria_agente.json'")
                    else:
                        print("❌ Erro ao exportar memória")
                    continue
                
                # Processar pergunta normal
                result = agent.process_user_input(user_input)
                
                print(f"\n📋 Resultado:")
                print(f"   • Tipo de decisão: {result['decision_type']}")
                print(f"   • Confiança: {result['confidence']:.2f}")
                print(f"   • Qualidade: {result['quality_metrics']['overall_score']:.2f}")
                
                if result.get('needs_human_help'):
                    print(f"\n🤔 {result['response']}")
                else:
                    print(f"\n💡 Análise:")
                    print(f"{result['response']}")
                
                # Mostrar dados utilizados
                if result.get('data_used'):
                    print(f"\n📊 Dados utilizados:")
                    for data in result['data_used']:
                        print(f"   • {data}")
                
            except KeyboardInterrupt:
                print(f"\n\n👋 Encerrando agente...")
                break
            except Exception as e:
                print(f"❌ Erro: {e}")
                continue
        
        # Limpar recursos
        agent.close()
        
    except Exception as e:
        print(f"❌ Erro fatal: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 