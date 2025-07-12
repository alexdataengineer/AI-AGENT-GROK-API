from typing import List, Dict, Any, Optional
from datetime import datetime
import json
from config import MAX_MEMORY_SIZE

class MemoryManager:
    def __init__(self):
        self.memory = []
        self.max_size = MAX_MEMORY_SIZE
    
    def add_interaction(self, user_input: str, agent_response: str, 
                       confidence: float, data_used: str = "", 
                       insights_generated: str = "") -> None:
        """
        Adiciona uma interação à memória do agente
        """
        interaction = {
            "timestamp": datetime.now().isoformat(),
            "user_input": user_input,
            "agent_response": agent_response,
            "confidence": confidence,
            "data_used": data_used,
            "insights_generated": insights_generated
        }
        
        self.memory.append(interaction)
        
        # Manter apenas as últimas MAX_MEMORY_SIZE interações
        if len(self.memory) > self.max_size:
            self.memory = self.memory[-self.max_size:]
    
    def get_recent_interactions(self, limit: int = 5) -> List[Dict[str, Any]]:
        """
        Retorna as interações mais recentes
        """
        return self.memory[-limit:] if self.memory else []
    
    def get_interactions_by_confidence(self, min_confidence: float = 0.0) -> List[Dict[str, Any]]:
        """
        Retorna interações com confiança acima do limite
        """
        return [interaction for interaction in self.memory 
                if interaction.get("confidence", 0) >= min_confidence]
    
    def get_memory_summary(self) -> Dict[str, Any]:
        """
        Retorna um resumo da memória
        """
        if not self.memory:
            return {"total_interactions": 0}
        
        confidences = [interaction.get("confidence", 0) for interaction in self.memory]
        
        return {
            "total_interactions": len(self.memory),
            "average_confidence": sum(confidences) / len(confidences),
            "min_confidence": min(confidences),
            "max_confidence": max(confidences),
            "recent_interactions": len(self.get_recent_interactions())
        }
    
    def search_memory(self, search_term: str) -> List[Dict[str, Any]]:
        """
        Busca na memória por termo específico
        """
        results = []
        search_term_lower = search_term.lower()
        
        for interaction in self.memory:
            if (search_term_lower in interaction.get("user_input", "").lower() or
                search_term_lower in interaction.get("agent_response", "").lower() or
                search_term_lower in interaction.get("insights_generated", "").lower()):
                results.append(interaction)
        
        return results
    
    def clear_memory(self) -> None:
        """
        Limpa toda a memória
        """
        self.memory = []
    
    def export_memory(self, filepath: str) -> bool:
        """
        Exporta a memória para um arquivo JSON
        """
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(self.memory, f, ensure_ascii=False, indent=2)
            return True
        except Exception as e:
            print(f"Erro ao exportar memória: {e}")
            return False
    
    def import_memory(self, filepath: str) -> bool:
        """
        Importa memória de um arquivo JSON
        """
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                imported_memory = json.load(f)
            
            # Validar formato
            if isinstance(imported_memory, list):
                self.memory.extend(imported_memory)
                # Manter limite de tamanho
                if len(self.memory) > self.max_size:
                    self.memory = self.memory[-self.max_size:]
                return True
            return False
        except Exception as e:
            print(f"Erro ao importar memória: {e}")
            return False 