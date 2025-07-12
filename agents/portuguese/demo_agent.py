#!/usr/bin/env python3
"""
Agente de Demonstração - Funciona offline
"""

import json
from typing import Dict, List, Any, Optional
from datetime import datetime
import random

class DemoGrokAPI:
    def __init__(self):
        # Respostas simuladas para demonstração
        self.responses = {
            "pib": [
                "Com base na análise dos dados, as 10 cidades com maior PIB são: São Paulo (R$ 500 bi), Rio de Janeiro (R$ 300 bi), Brasília (R$ 250 bi), Belo Horizonte (R$ 200 bi), Curitiba (R$ 180 bi), Porto Alegre (R$ 150 bi), Salvador (R$ 120 bi), Fortaleza (R$ 100 bi), Recife (R$ 90 bi) e Goiânia (R$ 80 bi).",
                "Análise do PIB das principais cidades: São Paulo lidera com R$ 500 bilhões, seguido pelo Rio de Janeiro com R$ 300 bilhões. A concentração econômica está claramente no Sudeste, que representa 65% do PIB total analisado.",
                "Ranking de PIB municipal: 1º São Paulo (R$ 500 bi), 2º Rio de Janeiro (R$ 300 bi), 3º Brasília (R$ 250 bi). Observa-se uma forte concentração econômica nas capitais estaduais."
            ],
            "busca": [
                "Informações sobre São Paulo: População de 12 milhões, PIB de R$ 500 bilhões, taxa de desemprego de 8.2%, índice de educação de 0.85. A cidade é o principal centro econômico do país.",
                "São Paulo - Capital econômica: 12 milhões de habitantes, PIB per capita de R$ 41.667, taxa de desemprego de 8.2%, índice de educação de 0.85. Maior centro financeiro da América Latina.",
                "Dados de São Paulo: 12 milhões de habitantes, PIB total de R$ 500 bilhões, representando 12% do PIB nacional. Taxa de desemprego de 8.2% e índice de educação de 0.85."
            ],
            "insights": [
                "Insights de negócio: O Sudeste concentra 65% do PIB, oferecendo oportunidades em logística e distribuição. Cidades com alto índice de educação (0.85+) apresentam melhor PIB per capita. Recomenda-se investir em cidades emergentes como Goiânia e Campinas.",
                "Oportunidades identificadas: 1) Expansão para cidades do interior com alto crescimento (Campinas, Goiânia), 2) Foco em regiões com baixa concorrência (Norte, Centro-Oeste), 3) Investimento em educação correlaciona com melhor performance econômica.",
                "Análise estratégica: Concentração econômica no Sudeste (65% do PIB) sugere saturação de mercado. Oportunidades em cidades emergentes do Centro-Oeste e interior do Sudeste. Correlação positiva entre educação e PIB per capita (r=0.78)."
            ],
            "correlacao": [
                "Correlação entre população e PIB: r=0.85 (forte correlação positiva). Cidades maiores tendem a ter PIB total maior, mas PIB per capita varia significativamente. São Paulo tem PIB per capita de R$ 41.667, enquanto Brasília tem R$ 83.333.",
                "Análise de correlação: População vs PIB total (r=0.85), PIB per capita vs educação (r=0.78), população vs desemprego (r=0.45). Maior população não necessariamente significa melhor PIB per capita.",
                "Correlações identificadas: População-PIB total (0.85), Educação-PIB per capita (0.78), População-desemprego (0.45). Cidades menores podem ter melhor eficiência econômica."
            ],
            "regioes": [
                "Comparação regional: Sudeste lidera com 65% do PIB, seguido pelo Nordeste (20%), Sul (10%) e Centro-Oeste (5%). O Sudeste tem maior PIB per capita (R$ 45.000) e menor taxa de desemprego (7.5%).",
                "Análise regional: Sudeste concentra 65% do PIB nacional, com PIB per capita de R$ 45.000. Nordeste tem 20% do PIB, mas menor PIB per capita (R$ 25.000). Sul apresenta melhor distribuição de renda.",
                "Comparação entre regiões: Sudeste (65% PIB, R$ 45k per capita), Nordeste (20% PIB, R$ 25k per capita), Sul (10% PIB, R$ 35k per capita), Centro-Oeste (5% PIB, R$ 30k per capita)."
            ]
        }
    
    def analyze_data_insights(self, data_summary: str, user_question: str) -> str:
        """
        Gera insights simulados baseados na pergunta
        """
        question_lower = user_question.lower()
        
        if "pib" in question_lower or "ranking" in question_lower or "maior" in question_lower:
            return random.choice(self.responses["pib"])
        elif "buscar" in question_lower or "são paulo" in question_lower or "encontrar" in question_lower:
            return random.choice(self.responses["busca"])
        elif "insight" in question_lower or "oportunidade" in question_lower or "negócio" in question_lower:
            return random.choice(self.responses["insights"])
        elif "correlação" in question_lower or "correlacao" in question_lower:
            return random.choice(self.responses["correlacao"])
        elif "região" in question_lower or "regioes" in question_lower or "comparar" in question_lower:
            return random.choice(self.responses["regioes"])
        else:
            return random.choice(self.responses["insights"])

class DemoDataManager:
    def __init__(self):
        # Dados simulados mais realistas
        self.sample_data = {
            "total_records": 200,
            "total_cities": 20,
            "total_states": 10,
            "total_regions": 5,
            "avg_population": 2500000,
            "avg_gdp_per_capita": 45000.0,
            "avg_unemployment": 8.5,
            "avg_education_index": 0.75
        }
        
        # Dados de cidades simulados
        self.cities_data = [
            {"cidade": "São Paulo", "estado": "SP", "regiao": "Sudeste", "populacao": 12000000, "pib_total": 500000000000, "pib_per_capita": 41667, "taxa_desemprego": 8.2, "indice_educacao": 0.85},
            {"cidade": "Rio de Janeiro", "estado": "RJ", "regiao": "Sudeste", "populacao": 6700000, "pib_total": 300000000000, "pib_per_capita": 44776, "taxa_desemprego": 9.1, "indice_educacao": 0.82},
            {"cidade": "Brasília", "estado": "DF", "regiao": "Centro-Oeste", "populacao": 3000000, "pib_total": 250000000000, "pib_per_capita": 83333, "taxa_desemprego": 6.8, "indice_educacao": 0.88},
            {"cidade": "Belo Horizonte", "estado": "MG", "regiao": "Sudeste", "populacao": 2500000, "pib_total": 200000000000, "pib_per_capita": 80000, "taxa_desemprego": 7.5, "indice_educacao": 0.80},
            {"cidade": "Curitiba", "estado": "PR", "regiao": "Sul", "populacao": 1900000, "pib_total": 180000000000, "pib_per_capita": 94737, "taxa_desemprego": 6.2, "indice_educacao": 0.87}
        ]
    
    def get_data_summary(self) -> Dict[str, Any]:
        return self.sample_data
    
    def search_cities(self, search_term: str) -> List[Dict[str, Any]]:
        results = []
        search_term_lower = search_term.lower()
        
        for city in self.cities_data:
            if (search_term_lower in city["cidade"].lower() or 
                search_term_lower in city["estado"].lower() or
                search_term_lower in city["regiao"].lower()):
                results.append(city)
        
        return results
    
    def analyze_by_region(self) -> List[Dict[str, Any]]:
        regions = {}
        
        for city in self.cities_data:
            region = city["regiao"]
            if region not in regions:
                regions[region] = {
                    "regiao": region,
                    "num_cidades": 0,
                    "populacao_total": 0,
                    "pib_total_regiao": 0,
                    "pib_per_capita_medio": 0,
                    "taxa_desemprego_media": 0
                }
            
            regions[region]["num_cidades"] += 1
            regions[region]["populacao_total"] += city["populacao"]
            regions[region]["pib_total_regiao"] += city["pib_total"]
        
        # Calcular médias
        for region_data in regions.values():
            if region_data["num_cidades"] > 0:
                region_data["pib_per_capita_medio"] = region_data["pib_total_regiao"] / region_data["populacao_total"]
        
        return list(regions.values())
    
    def get_top_cities(self, metric: str = "pib_total", limit: int = 5) -> List[Dict[str, Any]]:
        sorted_cities = sorted(self.cities_data, key=lambda x: x[metric], reverse=True)
        return sorted_cities[:limit]

class DemoMemoryManager:
    def __init__(self):
        self.memory = []
        self.max_size = 1000
    
    def add_interaction(self, user_input: str, agent_response: str, confidence: float) -> None:
        interaction = {
            "timestamp": datetime.now().isoformat(),
            "user_input": user_input,
            "agent_response": agent_response,
            "confidence": confidence
        }
        
        self.memory.append(interaction)
        
        if len(self.memory) > self.max_size:
            self.memory = self.memory[-self.max_size:]
    
    def get_memory_summary(self) -> Dict[str, Any]:
        if not self.memory:
            return {"total_interactions": 0}
        
        confidences = [interaction.get("confidence", 0) for interaction in self.memory]
        
        return {
            "total_interactions": len(self.memory),
            "average_confidence": sum(confidences) / len(confidences),
            "min_confidence": min(confidences),
            "max_confidence": max(confidences)
        }
    
    def search_memory(self, search_term: str) -> List[Dict[str, Any]]:
        results = []
        search_term_lower = search_term.lower()
        
        for interaction in self.memory:
            if (search_term_lower in interaction.get("user_input", "").lower() or
                search_term_lower in interaction.get("agent_response", "").lower()):
                results.append(interaction)
        
        return results

class DemoDataAnalysisAgent:
    def __init__(self):
        """
        Inicializa o agente de demonstração
        """
        self.grok_api = DemoGrokAPI()
        self.data_manager = DemoDataManager()
        self.memory_manager = DemoMemoryManager()
        
        print("🤖 Agente de Demonstração inicializado!")
        print("📊 Dados simulados carregados (200 registros)")
        print("🧠 Sistema de memória ativo")
        print("🔄 Loop de decisão configurado")
        print("👥 Sistema human-in-the-loop ativo")
    
    def process_user_input(self, user_input: str) -> Dict[str, Any]:
        """
        Processa a entrada do usuário
        """
        print(f"\n🔍 Analisando entrada: {user_input}")
        
        # Determinar tipo de análise
        if "pib" in user_input.lower() or "ranking" in user_input.lower() or "maior" in user_input.lower():
            decision_type = "data_analysis"
            confidence = 0.85
        elif "buscar" in user_input.lower() or "encontrar" in user_input.lower():
            decision_type = "data_search"
            confidence = 0.80
        elif "insight" in user_input.lower() or "oportunidade" in user_input.lower():
            decision_type = "insight_generation"
            confidence = 0.90
        elif "correlação" in user_input.lower() or "correlacao" in user_input.lower():
            decision_type = "correlation_analysis"
            confidence = 0.75
        elif "região" in user_input.lower() or "regioes" in user_input.lower():
            decision_type = "regional_analysis"
            confidence = 0.80
        else:
            decision_type = "data_analysis"
            confidence = 0.70
        
        print(f"📋 Tipo de decisão: {decision_type}")
        print(f"🎯 Confiança: {confidence:.2f}")
        
        # Verificar se precisa de ajuda humana
        if confidence < 0.7:
            return self._request_human_help(user_input, "Confiança baixa", confidence)
        
        # Executar análise
        if decision_type == "data_search":
            search_results = self.data_manager.search_cities("São Paulo")
            data_summary = f"Busca realizada: {len(search_results)} resultados encontrados"
        elif decision_type == "regional_analysis":
            region_data = self.data_manager.analyze_by_region()
            data_summary = f"Análise regional: {len(region_data)} regiões analisadas"
        else:
            summary = self.data_manager.get_data_summary()
            data_summary = f"Dados disponíveis: {summary['total_records']} registros"
        
        # Gerar resposta
        response = self.grok_api.analyze_data_insights(data_summary, user_input)
        
        # Avaliar qualidade
        quality_metrics = {
            "response_length": len(response),
            "confidence_score": confidence,
            "has_insights": "insight" in response.lower() or "oportunidade" in response.lower(),
            "has_data": any(word in response.lower() for word in ["milhões", "bilhões", "r$"]),
            "overall_score": min(confidence + 0.1, 1.0)
        }
        
        # Salvar na memória
        self.memory_manager.add_interaction(user_input, response, confidence)
        
        return {
            "response": response,
            "confidence": confidence,
            "decision_type": decision_type,
            "quality_metrics": quality_metrics,
            "data_used": data_summary,
            "needs_human_help": False
        }
    
    def _request_human_help(self, user_input: str, reason: str, confidence: float) -> Dict[str, Any]:
        """
        Solicita ajuda humana
        """
        help_message = f"""
        🤔 **Solicitação de Ajuda Humana**
        
        **Pergunta:** {user_input}
        **Motivo:** {reason}
        **Confiança:** {confidence:.2f}
        
        O agente não tem confiança suficiente para executar esta análise automaticamente.
        Por favor, forneça orientações específicas ou reformule a pergunta.
        """
        
        return {
            "response": help_message,
            "confidence": confidence,
            "decision_type": "human_assistance",
            "quality_metrics": {"overall_score": confidence},
            "needs_human_help": True,
            "help_reason": reason
        }
    
    def get_data_overview(self) -> Dict[str, Any]:
        return self.data_manager.get_data_summary()
    
    def get_memory_summary(self) -> Dict[str, Any]:
        return self.memory_manager.get_memory_summary()
    
    def search_memory(self, search_term: str) -> List[Dict[str, Any]]:
        return self.memory_manager.search_memory(search_term)
    
    def clear_memory(self) -> None:
        self.memory_manager.memory = []
        print("🧠 Memória limpa!")
    
    def export_memory(self, filepath: str) -> bool:
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(self.memory_manager.memory, f, ensure_ascii=False, indent=2)
            return True
        except Exception as e:
            print(f"Erro ao exportar: {e}")
            return False

def main():
    """
    Função principal para demonstração
    """
    print("🚀 Iniciando Agente de Demonstração...")
    
    try:
        agent = DemoDataAnalysisAgent()
        
        # Mostrar dados
        data_overview = agent.get_data_overview()
        print(f"\n📊 Visão Geral dos Dados:")
        print(f"   • Total de registros: {data_overview['total_records']}")
        print(f"   • Cidades únicas: {data_overview['total_cities']}")
        print(f"   • Estados: {data_overview['total_states']}")
        print(f"   • Regiões: {data_overview['total_regions']}")
        print(f"   • População média: {data_overview['avg_population']:,.0f}")
        print(f"   • PIB per capita médio: R$ {data_overview['avg_gdp_per_capita']:,.2f}")
        
        print(f"\n💡 Exemplos de perguntas:")
        print(f"   • 'Quais são as 10 cidades com maior PIB?'")
        print(f"   • 'Analise a correlação entre população e PIB'")
        print(f"   • 'Compare as regiões do Brasil'")
        print(f"   • 'Busque informações sobre São Paulo'")
        print(f"   • 'Gere insights sobre oportunidades de negócio'")
        
        print(f"\n🔧 Comandos especiais:")
        print(f"   • 'memoria' - Ver resumo da memória")
        print(f"   • 'limpar' - Limpar memória")
        print(f"   • 'exportar' - Exportar memória")
        print(f"   • 'sair' - Encerrar programa")
        
        # Loop principal
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
                    success = agent.export_memory("memoria_demo.json")
                    if success:
                        print("✅ Memória exportada para 'memoria_demo.json'")
                    else:
                        print("❌ Erro ao exportar memória")
                    continue
                
                # Processar pergunta
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
                    print(f"   • {result['data_used']}")
                
            except KeyboardInterrupt:
                print(f"\n\n👋 Encerrando agente...")
                break
            except Exception as e:
                print(f"❌ Erro: {e}")
                continue
        
    except Exception as e:
        print(f"❌ Erro fatal: {e}")

if __name__ == "__main__":
    main() 