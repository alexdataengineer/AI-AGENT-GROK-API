from typing import Dict, List, Any, Tuple
from enum import Enum
import re

class DecisionType(Enum):
    DATA_ANALYSIS = "data_analysis"
    DATA_SEARCH = "data_search"
    INSIGHT_GENERATION = "insight_generation"
    HUMAN_ASSISTANCE = "human_assistance"
    MEMORY_SEARCH = "memory_search"
    UNKNOWN = "unknown"

class DecisionEngine:
    def __init__(self, confidence_threshold: float = 0.7):
        self.confidence_threshold = confidence_threshold
        
        # Padrões para identificar tipos de decisão
        self.patterns = {
            DecisionType.DATA_ANALYSIS: [
                r"analis[ae]r?",
                r"estatístic[ao]s?",
                r"média",
                r"correlação",
                r"tendência",
                r"comparar",
                r"ranking",
                r"top",
                r"melhor",
                r"pior"
            ],
            DecisionType.DATA_SEARCH: [
                r"buscar",
                r"encontrar",
                r"procurar",
                r"cidade",
                r"estado",
                r"região",
                r"específic[ao]",
                r"filtro"
            ],
            DecisionType.INSIGHT_GENERATION: [
                r"insight",
                r"conclusão",
                r"recomendação",
                r"análise de negócio",
                r"business intelligence",
                r"estratégia",
                r"oportunidade",
                r"risco"
            ],
            DecisionType.MEMORY_SEARCH: [
                r"lembrar",
                r"anterior",
                r"última",
                r"histórico",
                r"passado",
                r"memória"
            ]
        }
    
    def analyze_user_input(self, user_input: str) -> Tuple[DecisionType, float, Dict[str, Any]]:
        """
        Analisa a entrada do usuário e determina o tipo de decisão
        """
        user_input_lower = user_input.lower()
        
        # Calcular confiança para cada tipo de decisão
        confidence_scores = {}
        
        for decision_type, patterns in self.patterns.items():
            score = 0
            for pattern in patterns:
                if re.search(pattern, user_input_lower):
                    score += 1
            
            # Normalizar score
            confidence_scores[decision_type] = min(score / len(patterns), 1.0)
        
        # Determinar o tipo de decisão com maior confiança
        best_type = max(confidence_scores.items(), key=lambda x: x[1])
        
        # Se nenhum padrão foi encontrado, classificar como análise de dados
        if best_type[1] == 0:
            best_type = (DecisionType.DATA_ANALYSIS, 0.3)
        
        # Extrair informações adicionais
        context = self._extract_context(user_input)
        
        return best_type[0], best_type[1], context
    
    def _extract_context(self, user_input: str) -> Dict[str, Any]:
        """
        Extrai contexto adicional da entrada do usuário
        """
        context = {
            "metrics": [],
            "regions": [],
            "cities": [],
            "time_period": None,
            "comparison_requested": False
        }
        
        # Identificar métricas mencionadas
        metrics = ["população", "pib", "desemprego", "educação", "pib per capita"]
        for metric in metrics:
            if metric in user_input.lower():
                context["metrics"].append(metric)
        
        # Identificar regiões
        regions = ["norte", "nordeste", "sudeste", "sul", "centro-oeste"]
        for region in regions:
            if region in user_input.lower():
                context["regions"].append(region)
        
        # Identificar cidades (padrão básico)
        city_pattern = r"\b[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*\b"
        cities = re.findall(city_pattern, user_input)
        context["cities"] = [city for city in cities if len(city) > 2]
        
        # Identificar solicitação de comparação
        comparison_words = ["comparar", "versus", "vs", "diferença", "comparação"]
        context["comparison_requested"] = any(word in user_input.lower() for word in comparison_words)
        
        return context
    
    def should_request_human_help(self, confidence: float, decision_type: DecisionType, 
                                 context: Dict[str, Any]) -> Tuple[bool, str]:
        """
        Decide se deve pedir ajuda humana
        """
        reasons = []
        
        # Confiança baixa
        if confidence < self.confidence_threshold:
            reasons.append(f"Confiança baixa ({confidence:.2f})")
        
        # Tipo de decisão desconhecido
        if decision_type == DecisionType.UNKNOWN:
            reasons.append("Tipo de análise não reconhecido")
        
        # Contexto muito complexo
        if len(context.get("metrics", [])) > 3:
            reasons.append("Muitas métricas solicitadas")
        
        if len(context.get("regions", [])) > 2 and len(context.get("cities", [])) > 2:
            reasons.append("Análise muito complexa (múltiplas regiões e cidades)")
        
        # Solicitação de comparação complexa
        if context.get("comparison_requested") and len(context.get("metrics", [])) > 2:
            reasons.append("Comparação complexa solicitada")
        
        should_help = len(reasons) > 0
        reason_text = "; ".join(reasons) if reasons else "Análise pode ser executada automaticamente"
        
        return should_help, reason_text
    
    def generate_action_plan(self, decision_type: DecisionType, confidence: float, 
                           context: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Gera um plano de ação baseado na decisão
        """
        actions = []
        
        if decision_type == DecisionType.DATA_ANALYSIS:
            actions.append({
                "action": "get_data_summary",
                "description": "Obter resumo estatístico dos dados",
                "priority": 1
            })
            
            if context.get("metrics"):
                for metric in context["metrics"]:
                    actions.append({
                        "action": "analyze_metric",
                        "description": f"Analisar métrica: {metric}",
                        "parameters": {"metric": metric},
                        "priority": 2
                    })
        
        elif decision_type == DecisionType.DATA_SEARCH:
            if context.get("cities"):
                actions.append({
                    "action": "search_cities",
                    "description": f"Buscar cidades: {', '.join(context['cities'])}",
                    "parameters": {"search_terms": context["cities"]},
                    "priority": 1
                })
            
            if context.get("regions"):
                actions.append({
                    "action": "analyze_by_region",
                    "description": f"Analisar regiões: {', '.join(context['regions'])}",
                    "parameters": {"regions": context["regions"]},
                    "priority": 2
                })
        
        elif decision_type == DecisionType.INSIGHT_GENERATION:
            actions.append({
                "action": "generate_insights",
                "description": "Gerar insights de negócio",
                "priority": 1
            })
            
            if context.get("comparison_requested"):
                actions.append({
                    "action": "comparative_analysis",
                    "description": "Realizar análise comparativa",
                    "priority": 2
                })
        
        elif decision_type == DecisionType.MEMORY_SEARCH:
            actions.append({
                "action": "search_memory",
                "description": "Buscar em interações anteriores",
                "priority": 1
            })
        
        # Ordenar ações por prioridade
        actions.sort(key=lambda x: x["priority"])
        
        return actions
    
    def evaluate_decision_quality(self, user_input: str, response: str, 
                                confidence: float) -> Dict[str, Any]:
        """
        Avalia a qualidade da decisão tomada
        """
        quality_metrics = {
            "response_length": len(response),
            "confidence_score": confidence,
            "has_insights": any(word in response.lower() for word in ["insight", "conclusão", "recomendação"]),
            "has_data": any(word in response.lower() for word in ["dados", "estatística", "número"]),
            "has_actions": any(word in response.lower() for word in ["ação", "estratégia", "próximo"])
        }
        
        # Calcular score geral
        score = 0
        if quality_metrics["has_insights"]: score += 0.3
        if quality_metrics["has_data"]: score += 0.3
        if quality_metrics["has_actions"]: score += 0.2
        score += min(confidence, 0.2)
        
        quality_metrics["overall_score"] = min(score, 1.0)
        
        return quality_metrics 