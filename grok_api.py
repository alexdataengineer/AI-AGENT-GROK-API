import requests
import json
from typing import List, Dict, Any
from config import XAI_API_KEY, XAI_API_URL

class GrokAPI:
    def __init__(self):
        self.api_key = XAI_API_KEY
        self.api_url = XAI_API_URL
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }
    
    def chat_completion(self, messages: List[Dict[str, str]], stream: bool = False) -> Dict[str, Any]:
        """
        Envia uma requisição para a API Grok
        """
        payload = {
            "messages": messages,
            "model": "grok-4",
            "stream": stream
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
    
    def evaluate_confidence(self, task_description: str, available_data: str) -> float:
        """
        Avalia a confiança do agente para executar uma tarefa
        """
        system_prompt = """Avalie sua confiança (0-1) para executar a tarefa descrita com os dados disponíveis.
        Considere: clareza da pergunta, qualidade dos dados, complexidade da análise.
        Responda apenas com um número entre 0 e 1."""
        
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"Tarefa: {task_description}\nDados disponíveis: {available_data}"}
        ]
        
        response = self.chat_completion(messages)
        
        if "error" in response:
            return 0.5  # Confiança média em caso de erro
        
        try:
            confidence = float(response.get("choices", [{}])[0].get("message", {}).get("content", "0.5"))
            return max(0.0, min(1.0, confidence))
        except ValueError:
            return 0.5 