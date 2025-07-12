import os
from dotenv import load_dotenv

load_dotenv()

# Configurações da API Grok
XAI_API_KEY = os.getenv('XAI_API_KEY')
XAI_API_URL = os.getenv('XAI_API_URL', "https://api.x.ai/v1/chat/completions")

# Configurações do DuckDB
DATABASE_PATH = os.getenv('DATABASE_PATH', "data_analysis.db")

# Configurações do agente
MAX_MEMORY_SIZE = int(os.getenv('MAX_MEMORY_SIZE', 1000))
CONFIDENCE_THRESHOLD = float(os.getenv('CONFIDENCE_THRESHOLD', 0.7))

# Validação da API key
if not XAI_API_KEY:
    raise ValueError(
        "XAI_API_KEY não encontrada! "
        "Crie um arquivo .env baseado no .env.example e adicione sua API key."
    ) 