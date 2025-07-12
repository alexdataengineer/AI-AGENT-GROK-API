#!/usr/bin/env python3
"""
Versão simplificada do Agente de Análise de Dados para teste
"""

import requests
import json
from typing import Dict, List, Any, Optional
from datetime import datetime

# Configurações
XAI_API_KEY = "xai-ALAspSpCmyKga42PSR4xQNmHjuj68ux2lDHUC8RS9SBPTNrTBe4ZSAZDE42PhI96tJqq7hjRstilmGWp"
XAI_API_URL = "https://api.x.ai/v1/chat/completions"

class SimpleGrokAPI:
    def __init__(self):
        self.api_key = XAI_API_KEY
        self.api_url = XAI_API_URL
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }
    
    def chat_completion(self, messages: List[Dict[str, str]]) -> Dict[str, Any]:
        """
        Envia uma requisição para a API Grok
        """
        payload = {
            "messages": messages,
            "model": "grok-4",
            "stream": False
        }
        
        try:
            response = requests.post(
                self.api_url,
                headers=self.headers,
                json=payload,
                timeout=30
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return {"error": f"Erro na API: {str(e)}"}
    
    def analyze_data_insights(self, data_summary: str, user_question: str) -> str:
        """
        Analisa dados e gera insights usando Grok
        """
        system_prompt = """Você é um especialista em análise de dados e business intelligence. 
        Analise os dados fornecidos e responda à pergunta do usuário com insights valiosos para o negócio.
        Seja específico, use números quando possível e sugira ações baseadas nos dados."""
        
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"Resumo dos dados: {data_summary}\n\nPergunta: {user_question}"}
        ]
        
        response = self.chat_completion(messages)
        
        if "error" in response:
            return f"Erro na análise: {response['error']}"
        
        return response.get("choices", [{}])[0].get("message", {}).get("content", "Não foi possível gerar análise")

class SimpleDataManager:
    def __init__(self):
        # Dados simulados de exemplo
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
    
    def get_data_summary(self) -> Dict[str, Any]:
        return self.sample_data
    
    def search_cities(self, search_term: str) -> List[Dict[str, Any]]:
        # Simular busca
        return [
            {"cidade": "São Paulo", "estado": "SP", "populacao": 12000000, "pib_total": 500000000000},
            {"cidade": "Rio de Janeiro", "estado": "RJ", "populacao": 6700000, "pib_total": 300000000000}
        ]
    
    def analyze_by_region(self) -> List[Dict[str, Any]]:
        # Simular análise por região
        return [
            {"regiao": "Sudeste", "num_cidades": 8, "pib_total_regiao": 800000000000},
            {"regiao": "Nordeste", "num_cidades": 6, "pib_total_regiao": 400000000000},
            {"regiao": "Sul", "num_cidades": 4, "pib_total_regiao": 300000000000}
        ]

class SimpleMemoryManager:
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

class SimpleDataAnalysisAgent:
    def __init__(self):
        """
        Inicializa o agente simplificado
        """
        self.grok_api = SimpleGrokAPI()
        self.data_manager = SimpleDataManager()
        self.memory_manager = SimpleMemoryManager()
        
        print("🤖 Agente Simplificado de Análise de Dados inicializado!")
        print("📊 Dados simulados carregados")
        print("🧠 Sistema de memória ativo")
        print("🌐 Integração com Grok API configurada")
    
    def process_user_input(self, user_input: str) -> Dict[str, Any]:
        """
        Processa a entrada do usuário
        """
        print(f"\n🔍 Analisando: {user_input}")
        
        # Determinar tipo de análise
        if "pib" in user_input.lower() or "ranking" in user_input.lower():
            decision_type = "data_analysis"
            confidence = 0.8
        elif "buscar" in user_input.lower() or "encontrar" in user_input.lower():
            decision_type = "data_search"
            confidence = 0.7
        elif "insight" in user_input.lower() or "análise" in user_input.lower():
            decision_type = "insight_generation"
            confidence = 0.9
        else:
            decision_type = "data_analysis"
            confidence = 0.6
        
        print(f"📋 Tipo: {decision_type}")
        print(f"🎯 Confiança: {confidence:.2f}")
        
        # Executar análise
        if decision_type == "data_search":
            search_results = self.data_manager.search_cities("São Paulo")
            data_summary = f"Busca realizada: {len(search_results)} resultados encontrados"
        elif decision_type == "insight_generation":
            data_summary = "Análise de insights de negócio"
        else:
            summary = self.data_manager.get_data_summary()
            data_summary = f"Dados disponíveis: {summary['total_records']} registros"
        
        # Gerar resposta usando Grok
        response = self.grok_api.analyze_data_insights(data_summary, user_input)
        
        # Salvar na memória
        self.memory_manager.add_interaction(user_input, response, confidence)
        
        return {
            "response": response,
            "confidence": confidence,
            "decision_type": decision_type,
            "quality_metrics": {"overall_score": confidence},
            "data_used": data_summary,
            "needs_human_help": False
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
    Função principal para testar o agente simplificado
    """
    print("🚀 Iniciando Agente Simplificado...")
    
    try:
        agent = SimpleDataAnalysisAgent()
        
        # Mostrar dados
        data_overview = agent.get_data_overview()
        print(f"\n📊 Dados: {data_overview['total_records']} registros")
        
        # Testar perguntas
        test_questions = [
            "Quais são as 10 cidades com maior PIB?",
            "Busque informações sobre São Paulo",
            "Gere insights sobre oportunidades de negócio"
        ]
        
        for question in test_questions:
            print(f"\n🤖 Pergunta: {question}")
            result = agent.process_user_input(question)
            print(f"✅ Resposta: {result['response'][:100]}...")
            print(f"📊 Confiança: {result['confidence']:.2f}")
        
        # Mostrar memória
        memory_summary = agent.get_memory_summary()
        print(f"\n🧠 Memória: {memory_summary['total_interactions']} interações")
        
        print("\n🎉 Teste concluído com sucesso!")
        
    except Exception as e:
        print(f"❌ Erro: {e}")

if __name__ == "__main__":
    main() 