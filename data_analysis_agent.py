from typing import Dict, List, Any, Optional, Tuple
import pandas as pd
from datetime import datetime

from grok_api import GrokAPI
from data_manager import DataManager
from memory_manager import MemoryManager
from decision_engine import DecisionEngine, DecisionType
from config import CONFIDENCE_THRESHOLD

class DataAnalysisAgent:
    def __init__(self):
        """
        Inicializa o agente de análise de dados com todas as funcionalidades
        """
        self.grok_api = GrokAPI()
        self.data_manager = DataManager()
        self.memory_manager = MemoryManager()
        self.decision_engine = DecisionEngine(confidence_threshold=CONFIDENCE_THRESHOLD)
        
        print("🤖 Agente de Análise de Dados inicializado!")
        print("📊 Banco de dados com 200 registros de cidades brasileiras carregado")
        print("🧠 Sistema de memória ativo")
        print("🔄 Loop de decisão configurado")
        print("👥 Sistema human-in-the-loop ativo")
    
    def process_user_input(self, user_input: str) -> Dict[str, Any]:
        """
        Processa a entrada do usuário e retorna uma resposta completa
        """
        print(f"\n🔍 Analisando entrada: {user_input}")
        
        # 1. Análise de decisão
        decision_type, confidence, context = self.decision_engine.analyze_user_input(user_input)
        print(f"📋 Tipo de decisão: {decision_type.value}")
        print(f"🎯 Confiança: {confidence:.2f}")
        
        # 2. Verificar se precisa de ajuda humana
        needs_help, help_reason = self.decision_engine.should_request_human_help(
            confidence, decision_type, context
        )
        
        if needs_help:
            return self._request_human_help(user_input, help_reason, confidence)
        
        # 3. Gerar plano de ação
        action_plan = self.decision_engine.generate_action_plan(decision_type, confidence, context)
        print(f"📝 Plano de ação: {len(action_plan)} ações")
        
        # 4. Executar ações
        results = self._execute_actions(action_plan, user_input)
        
        # 5. Gerar resposta final
        final_response = self._generate_final_response(user_input, results, confidence)
        
        # 6. Avaliar qualidade da decisão
        quality_metrics = self.decision_engine.evaluate_decision_quality(
            user_input, final_response, confidence
        )
        
        # 7. Salvar na memória
        self.memory_manager.add_interaction(
            user_input=user_input,
            agent_response=final_response,
            confidence=confidence,
            data_used=str(results.get("data_used", "")),
            insights_generated=str(results.get("insights", ""))
        )
        
        return {
            "response": final_response,
            "confidence": confidence,
            "decision_type": decision_type.value,
            "quality_metrics": quality_metrics,
            "data_used": results.get("data_used", ""),
            "insights": results.get("insights", ""),
            "needs_human_help": False
        }
    
    def _execute_actions(self, action_plan: List[Dict[str, Any]], user_input: str) -> Dict[str, Any]:
        """
        Executa o plano de ação
        """
        results = {
            "data_used": [],
            "insights": [],
            "raw_data": {}
        }
        
        for action in action_plan:
            action_name = action.get("action")
            parameters = action.get("parameters", {})
            
            print(f"⚡ Executando: {action.get('description', action_name)}")
            
            if action_name == "get_data_summary":
                summary = self.data_manager.get_data_summary()
                results["data_used"].append("Resumo estatístico geral")
                results["raw_data"]["summary"] = summary
            
            elif action_name == "analyze_metric":
                metric = parameters.get("metric", "")
                if "pib" in metric.lower():
                    top_cities = self.data_manager.get_top_cities("pib_total", 10)
                    results["data_used"].append(f"Top 10 cidades por PIB")
                    results["raw_data"]["top_pib"] = top_cities
                elif "população" in metric.lower():
                    top_cities = self.data_manager.get_top_cities("populacao", 10)
                    results["data_used"].append(f"Top 10 cidades por população")
                    results["raw_data"]["top_population"] = top_cities
            
            elif action_name == "search_cities":
                search_terms = parameters.get("search_terms", [])
                for term in search_terms:
                    search_results = self.data_manager.search_cities(term)
                    results["data_used"].append(f"Busca por: {term}")
                    results["raw_data"][f"search_{term}"] = search_results
            
            elif action_name == "analyze_by_region":
                regions = parameters.get("regions", [])
                region_analysis = self.data_manager.analyze_by_region()
                results["data_used"].append("Análise por região")
                results["raw_data"]["region_analysis"] = region_analysis
            
            elif action_name == "generate_insights":
                # Usar Grok para gerar insights
                data_summary = str(results.get("raw_data", {}))
                insights = self.grok_api.analyze_data_insights(data_summary, user_input)
                results["insights"].append(insights)
            
            elif action_name == "comparative_analysis":
                correlation = self.data_manager.get_correlation_analysis()
                results["data_used"].append("Análise de correlação")
                results["raw_data"]["correlation"] = correlation
            
            elif action_name == "search_memory":
                memory_results = self.memory_manager.search_memory(user_input)
                results["data_used"].append("Busca na memória")
                results["raw_data"]["memory_search"] = memory_results
        
        return results
    
    def _generate_final_response(self, user_input: str, results: Dict[str, Any], 
                               confidence: float) -> str:
        """
        Gera a resposta final usando Grok
        """
        # Preparar dados para análise
        data_summary = []
        
        for data_type, data in results.get("raw_data", {}).items():
            if isinstance(data, dict):
                data_summary.append(f"{data_type}: {str(data)}")
            elif isinstance(data, pd.DataFrame) and not data.empty:
                data_summary.append(f"{data_type}: {data.to_string()}")
        
        data_text = "\n".join(data_summary)
        
        # Gerar resposta usando Grok
        system_prompt = """Você é um especialista em análise de dados e business intelligence.
        Analise os dados fornecidos e responda à pergunta do usuário de forma clara e objetiva.
        Inclua insights relevantes e recomendações quando apropriado."""
        
        user_prompt = f"""
        Pergunta do usuário: {user_input}
        
        Dados disponíveis:
        {data_text}
        
        Insights gerados:
        {'; '.join(results.get('insights', []))}
        
        Por favor, forneça uma análise completa e insights de negócio.
        """
        
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]
        
        response = self.grok_api.chat_completion(messages)
        
        if "error" in response:
            return f"Erro na análise: {response['error']}"
        
        return response.get("choices", [{}])[0].get("message", {}).get("content", 
               "Não foi possível gerar análise")
    
    def _request_human_help(self, user_input: str, reason: str, confidence: float) -> Dict[str, Any]:
        """
        Solicita ajuda humana quando necessário
        """
        help_message = f"""
        🤔 **Solicitação de Ajuda Humana**
        
        **Pergunta do usuário:** {user_input}
        **Motivo:** {reason}
        **Confiança do agente:** {confidence:.2f}
        
        O agente não tem confiança suficiente para executar esta análise automaticamente.
        Por favor, forneça orientações específicas ou reformule a pergunta.
        
        **Opções disponíveis:**
        1. Reformular a pergunta de forma mais específica
        2. Solicitar análise de métricas específicas
        3. Fornecer contexto adicional
        4. Executar análise com confiança reduzida
        """
        
        return {
            "response": help_message,
            "confidence": confidence,
            "decision_type": "human_assistance",
            "quality_metrics": {"overall_score": confidence},
            "needs_human_help": True,
            "help_reason": reason
        }
    
    def get_memory_summary(self) -> Dict[str, Any]:
        """
        Retorna um resumo da memória do agente
        """
        return self.memory_manager.get_memory_summary()
    
    def search_memory(self, search_term: str) -> List[Dict[str, Any]]:
        """
        Busca na memória do agente
        """
        return self.memory_manager.search_memory(search_term)
    
    def export_memory(self, filepath: str) -> bool:
        """
        Exporta a memória para um arquivo
        """
        return self.memory_manager.export_memory(filepath)
    
    def clear_memory(self) -> None:
        """
        Limpa a memória do agente
        """
        self.memory_manager.clear_memory()
        print("🧠 Memória do agente limpa!")
    
    def get_data_overview(self) -> Dict[str, Any]:
        """
        Retorna uma visão geral dos dados disponíveis
        """
        summary = self.data_manager.get_data_summary()
        return {
            "total_records": summary.get("total_registros", 0),
            "total_cities": summary.get("total_cidades", 0),
            "total_states": summary.get("total_estados", 0),
            "total_regions": summary.get("total_regioes", 0),
            "avg_population": summary.get("populacao_media", 0),
            "avg_gdp_per_capita": summary.get("pib_per_capita_medio", 0),
            "avg_unemployment": summary.get("taxa_desemprego_media", 0),
            "avg_education_index": summary.get("indice_educacao_medio", 0)
        }
    
    def close(self):
        """
        Fecha as conexões e limpa recursos
        """
        self.data_manager.close()
        print("🔒 Conexões fechadas e recursos liberados!") 