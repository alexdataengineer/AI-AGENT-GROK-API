#!/usr/bin/env python3
"""
Streamlit App Simplificado - Agente de Análise de Dados
"""

import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime
import json

# Importar o agente final
from final_agent import FinalDataAnalysisAgent

# Configuração da página
st.set_page_config(
    page_title="Agente de Análise de Dados",
    page_icon="🤖",
    layout="wide"
)

# Inicializar o agente
@st.cache_resource
def get_agent():
    return FinalDataAnalysisAgent()

def main():
    st.title("🤖 Agente de Análise de Dados")
    st.markdown("**Análise inteligente de dados com memória e Grok API**")
    
    agent = get_agent()
    
    # Sidebar
    st.sidebar.header("🔧 Controles")
    
    # Abas principais
    tab1, tab2, tab3 = st.tabs(["💬 Chat", "📊 Dados", "🧠 Memória"])
    
    with tab1:
        st.header("💬 Chat com o Agente")
        
        # Área de chat
        if "messages" not in st.session_state:
            st.session_state.messages = []
        
        # Mostrar mensagens anteriores
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])
        
        # Input do usuário
        if prompt := st.chat_input("Digite sua pergunta..."):
            # Adicionar mensagem do usuário
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)
            
            # Processar com o agente
            with st.chat_message("assistant"):
                with st.spinner("🤖 Analisando..."):
                    try:
                        result = agent.process_user_input(prompt)
                        
                        # Mostrar resultado
                        if result.get('needs_human_help'):
                            st.warning(result['response'])
                        else:
                            st.success("✅ Análise concluída!")
                            st.markdown(result['response'])
                            
                            # Mostrar métricas
                            col1, col2, col3 = st.columns(3)
                            with col1:
                                st.metric("Confiança", f"{result['confidence']:.2f}")
                            with col2:
                                st.metric("Qualidade", f"{result['quality_metrics']['overall_score']:.2f}")
                            with col3:
                                st.metric("Tipo", result['decision_type'])
                        
                        # Adicionar resposta à sessão
                        st.session_state.messages.append({
                            "role": "assistant", 
                            "content": result['response']
                        })
                        
                    except Exception as e:
                        st.error(f"❌ Erro na análise: {str(e)}")
                        st.session_state.messages.append({
                            "role": "assistant", 
                            "content": f"Desculpe, ocorreu um erro: {str(e)}"
                        })
    
    with tab2:
        st.header("📊 Visão Geral dos Dados")
        
        # Estatísticas gerais
        data_overview = agent.get_data_overview()
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Total de Registros", data_overview['total_records'])
        with col2:
            st.metric("Cidades Únicas", data_overview['total_cities'])
        with col3:
            st.metric("Estados", data_overview['total_states'])
        with col4:
            st.metric("Regiões", data_overview['total_regions'])
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("População Média", f"{data_overview['avg_population']:,.0f}")
        with col2:
            st.metric("PIB per Capita Médio", f"R$ {data_overview['avg_gdp_per_capita']:,.2f}")
        with col3:
            st.metric("Taxa de Desemprego Média", f"{data_overview['avg_unemployment']:.1f}%")
        with col4:
            st.metric("Índice de Educação Médio", f"{data_overview['avg_education_index']:.3f}")
        
        # Dados das principais cidades
        st.subheader("🏙️ Principais Cidades")
        
        cities_data = [
            {"cidade": "São Paulo", "estado": "SP", "regiao": "Sudeste", "populacao": 12000000, "pib_total": 500000000000, "pib_per_capita": 41667, "taxa_desemprego": 8.2, "indice_educacao": 0.85},
            {"cidade": "Rio de Janeiro", "estado": "RJ", "regiao": "Sudeste", "populacao": 6700000, "pib_total": 300000000000, "pib_per_capita": 44776, "taxa_desemprego": 9.1, "indice_educacao": 0.82},
            {"cidade": "Brasília", "estado": "DF", "regiao": "Centro-Oeste", "populacao": 3000000, "pib_total": 250000000000, "pib_per_capita": 83333, "taxa_desemprego": 6.8, "indice_educacao": 0.88},
            {"cidade": "Belo Horizonte", "estado": "MG", "regiao": "Sudeste", "populacao": 2500000, "pib_total": 200000000000, "pib_per_capita": 80000, "taxa_desemprego": 7.5, "indice_educacao": 0.80},
            {"cidade": "Curitiba", "estado": "PR", "regiao": "Sul", "populacao": 1900000, "pib_total": 180000000000, "pib_per_capita": 94737, "taxa_desemprego": 6.2, "indice_educacao": 0.87}
        ]
        
        df_cities = pd.DataFrame(cities_data)
        
        # Gráfico de PIB
        fig_pib = px.bar(
            df_cities,
            x='cidade',
            y='pib_total',
            title="PIB Total das Principais Cidades",
            labels={'pib_total': 'PIB Total (R$)', 'cidade': 'Cidade'}
        )
        st.plotly_chart(fig_pib, use_container_width=True)
        
        # Tabela de dados
        st.dataframe(df_cities, use_container_width=True)
    
    with tab3:
        st.header("🧠 Memória do Agente")
        
        # Resumo da memória
        memory_summary = agent.get_memory_summary()
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Total de Interações", memory_summary.get('total_interactions', 0))
        with col2:
            if memory_summary.get('total_interactions', 0) > 0:
                st.metric("Confiança Média", f"{memory_summary.get('average_confidence', 0):.2f}")
            else:
                st.metric("Confiança Média", "N/A")
        with col3:
            if memory_summary.get('total_interactions', 0) > 0:
                st.metric("Confiança Mínima", f"{memory_summary.get('min_confidence', 0):.2f}")
            else:
                st.metric("Confiança Mínima", "N/A")
        with col4:
            if memory_summary.get('total_interactions', 0) > 0:
                st.metric("Confiança Máxima", f"{memory_summary.get('max_confidence', 0):.2f}")
            else:
                st.metric("Confiança Máxima", "N/A")
        
        # Controles de memória
        st.subheader("⚙️ Gerenciar Memória")
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("🗑️ Limpar Memória"):
                agent.clear_memory()
                st.success("Memória limpa!")
                st.rerun()
        
        with col2:
            if st.button("💾 Exportar Memória"):
                success = agent.export_memory("memoria_agente.json")
                if success:
                    st.success("Memória exportada para 'memoria_agente.json'")
                else:
                    st.error("Erro ao exportar memória")
        
        # Exemplos de perguntas
        st.subheader("💡 Exemplos de Perguntas")
        st.info("""
        **Perguntas que funcionam bem:**
        • "Qual o PIB de Belo Horizonte?"
        • "São Paulo vs Rio de Janeiro, qual é melhor?"
        • "Quais são as 10 cidades com maior PIB?"
        • "Analise a correlação entre população e PIB"
        • "Compare as regiões do Brasil"
        • "Gere insights sobre oportunidades de negócio"
        """)

if __name__ == "__main__":
    main() 