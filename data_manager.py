import duckdb
import pandas as pd
import numpy as np
from typing import Dict, List, Any, Optional
from config import DATABASE_PATH
import os

class DataManager:
    def __init__(self):
        self.db_path = DATABASE_PATH
        self.conn = duckdb.connect(self.db_path)
        self._create_sample_data()
    
    def _create_sample_data(self):
        """
        Cria dados de exemplo com cidades, PIB e outras informações
        """
        # Dados de exemplo com 200 linhas
        np.random.seed(42)
        
        cities = [
            "São Paulo", "Rio de Janeiro", "Brasília", "Salvador", "Fortaleza",
            "Belo Horizonte", "Manaus", "Curitiba", "Recife", "Porto Alegre",
            "Goiânia", "Guarulhos", "Campinas", "Natal", "Maceió",
            "Teresina", "João Pessoa", "Campo Grande", "Petrópolis", "Vitória"
        ]
        
        states = [
            "SP", "RJ", "DF", "BA", "CE", "MG", "AM", "PR", "PE", "RS",
            "GO", "SP", "SP", "RN", "AL", "PI", "PB", "MS", "RJ", "ES"
        ]
        
        regions = [
            "Sudeste", "Sudeste", "Centro-Oeste", "Nordeste", "Nordeste",
            "Sudeste", "Norte", "Sul", "Nordeste", "Sul",
            "Centro-Oeste", "Sudeste", "Sudeste", "Nordeste", "Nordeste",
            "Nordeste", "Nordeste", "Centro-Oeste", "Sudeste", "Sudeste"
        ]
        
        # Gerar 200 registros
        data = []
        for i in range(200):
            city_idx = i % len(cities)
            population = np.random.randint(100000, 5000000)
            gdp_per_capita = np.random.uniform(15000, 80000)
            gdp_total = population * gdp_per_capita
            unemployment_rate = np.random.uniform(5, 15)
            education_index = np.random.uniform(0.6, 0.95)
            
            data.append({
                "id": i + 1,
                "cidade": cities[city_idx],
                "estado": states[city_idx],
                "regiao": regions[city_idx],
                "populacao": population,
                "pib_per_capita": round(gdp_per_capita, 2),
                "pib_total": round(gdp_total, 2),
                "taxa_desemprego": round(unemployment_rate, 2),
                "indice_educacao": round(education_index, 3),
                "ano": 2023
            })
        
        df = pd.DataFrame(data)
        
        # Criar tabela se não existir
        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS cidades_brasil (
                id INTEGER,
                cidade VARCHAR,
                estado VARCHAR,
                regiao VARCHAR,
                populacao INTEGER,
                pib_per_capita DOUBLE,
                pib_total DOUBLE,
                taxa_desemprego DOUBLE,
                indice_educacao DOUBLE,
                ano INTEGER
            )
        """)
        
        # Inserir dados
        self.conn.execute("DELETE FROM cidades_brasil")
        self.conn.execute("INSERT INTO cidades_brasil SELECT * FROM df")
        self.conn.commit()
    
    def execute_query(self, query: str) -> pd.DataFrame:
        """
        Executa uma consulta SQL no DuckDB
        """
        try:
            result = self.conn.execute(query).fetchdf()
            return result
        except Exception as e:
            return pd.DataFrame({"error": [str(e)]})
    
    def get_data_summary(self) -> Dict[str, Any]:
        """
        Retorna um resumo estatístico dos dados
        """
        summary_query = """
        SELECT 
            COUNT(*) as total_registros,
            COUNT(DISTINCT cidade) as total_cidades,
            COUNT(DISTINCT estado) as total_estados,
            COUNT(DISTINCT regiao) as total_regioes,
            AVG(populacao) as populacao_media,
            AVG(pib_per_capita) as pib_per_capita_medio,
            AVG(taxa_desemprego) as taxa_desemprego_media,
            AVG(indice_educacao) as indice_educacao_medio,
            SUM(pib_total) as pib_total_geral
        FROM cidades_brasil
        """
        
        result = self.execute_query(summary_query)
        return result.to_dict('records')[0] if not result.empty else {}
    
    def analyze_by_region(self) -> pd.DataFrame:
        """
        Análise por região
        """
        query = """
        SELECT 
            regiao,
            COUNT(*) as num_cidades,
            AVG(populacao) as populacao_media,
            AVG(pib_per_capita) as pib_per_capita_medio,
            AVG(taxa_desemprego) as taxa_desemprego_media,
            SUM(pib_total) as pib_total_regiao
        FROM cidades_brasil
        GROUP BY regiao
        ORDER BY pib_total_regiao DESC
        """
        return self.execute_query(query)
    
    def get_top_cities(self, metric: str = "pib_total", limit: int = 10) -> pd.DataFrame:
        """
        Retorna as top cidades por uma métrica específica
        """
        valid_metrics = ["pib_total", "populacao", "pib_per_capita", "indice_educacao"]
        if metric not in valid_metrics:
            metric = "pib_total"
        
        query = f"""
        SELECT cidade, estado, {metric}
        FROM cidades_brasil
        ORDER BY {metric} DESC
        LIMIT {limit}
        """
        return self.execute_query(query)
    
    def search_cities(self, search_term: str) -> pd.DataFrame:
        """
        Busca cidades por nome
        """
        query = f"""
        SELECT *
        FROM cidades_brasil
        WHERE LOWER(cidade) LIKE LOWER('%{search_term}%')
        OR LOWER(estado) LIKE LOWER('%{search_term}%')
        """
        return self.execute_query(query)
    
    def get_correlation_analysis(self) -> Dict[str, float]:
        """
        Análise de correlação entre variáveis
        """
        query = """
        SELECT 
            CORR(populacao, pib_total) as corr_pop_pib,
            CORR(pib_per_capita, indice_educacao) as corr_pib_educacao,
            CORR(taxa_desemprego, indice_educacao) as corr_desemprego_educacao,
            CORR(populacao, taxa_desemprego) as corr_pop_desemprego
        FROM cidades_brasil
        """
        result = self.execute_query(query)
        return result.to_dict('records')[0] if not result.empty else {}
    
    def close(self):
        """
        Fecha a conexão com o banco
        """
        self.conn.close() 