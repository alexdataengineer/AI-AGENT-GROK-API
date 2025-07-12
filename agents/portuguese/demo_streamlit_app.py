import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import json

# Importar o agente de demonstração
from demo_agent import DemoDataAnalysisAgent

# Configuração da página
st.set_page_config(
    page_title="🤖 Agente de Análise de Dados",
    page_icon="🤖",
    layout="wide"
)

# Inicializar o agente
@st.cache_resource
def get_agent():
    return DemoDataAnalysisAgent()

def main():
    st.title("🤖 Agente de Análise de Dados")
    st.markdown("**Análise inteligente de dados com memória, loop de decisão e human-in-the-loop**")
    
    agent = get_agent()
    
    # Sidebar
    st.sidebar.header("🔧 Controles")
    
    # Abas principais
    tab1, tab2, tab3, tab4 = st.tabs(["💬 Chat", "📊 Dados", "🧠 Memória", "⚙️ Configurações"])
    
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
        
        # Análise por região
        st.subheader("📈 Análise por Região")
        
        # Buscar dados de região
        region_data = agent.data_manager.analyze_by_region()
        
        if region_data:
            # Converter para DataFrame
            df_regions = pd.DataFrame(region_data)
            
            # Gráfico de barras para PIB por região
            fig_pib = px.bar(
                df_regions, 
                x='regiao', 
                y='pib_total_regiao',
                title="PIB Total por Região",
                labels={'pib_total_regiao': 'PIB Total (R$)', 'regiao': 'Região'}
            )
            st.plotly_chart(fig_pib, use_container_width=True)
            
            # Gráfico de pizza para distribuição de cidades
            fig_cidades = px.pie(
                df_regions,
                values='num_cidades',
                names='regiao',
                title="Distribuição de Cidades por Região"
            )
            st.plotly_chart(fig_cidades, use_container_width=True)
            
            # Tabela de dados
            st.dataframe(df_regions, use_container_width=True)
        
        # Dados das cidades
        st.subheader("🏙️ Dados das Cidades")
        
        cities_data = agent.data_manager.cities_data
        if cities_data:
            df_cities = pd.DataFrame(cities_data)
            
            # Gráfico de dispersão: População vs PIB
            fig_scatter = px.scatter(
                df_cities,
                x='populacao',
                y='pib_total',
                size='pib_per_capita',
                color='regiao',
                hover_name='cidade',
                title="População vs PIB Total (Tamanho = PIB per Capita)"
            )
            st.plotly_chart(fig_scatter, use_container_width=True)
            
            # Tabela das cidades
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
        
        # Busca na memória
        st.subheader("🔍 Buscar na Memória")
        search_term = st.text_input("Digite um termo para buscar na memória:")
        
        if search_term:
            memory_results = agent.search_memory(search_term)
            
            if memory_results:
                st.success(f"Encontradas {len(memory_results)} interações")
                
                for i, interaction in enumerate(memory_results):
                    with st.expander(f"Interação {i+1} - {interaction.get('timestamp', 'N/A')}"):
                        st.write(f"**Pergunta:** {interaction.get('user_input', 'N/A')}")
                        st.write(f"**Resposta:** {interaction.get('agent_response', 'N/A')}")
                        st.write(f"**Confiança:** {interaction.get('confidence', 0):.2f}")
            else:
                st.info("Nenhuma interação encontrada com esse termo.")
        
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
    
    with tab4:
        st.header("⚙️ Configurações")
        
        st.subheader("🔧 Configurações do Agente")
        
        # Informações sobre o agente
        st.info("""
        **Funcionalidades do Agente:**
        - ✅ Memória persistente com 1000 interações
        - ✅ Loop de decisão inteligente
        - ✅ Integração com Grok API
        - ✅ Análise de dados com DuckDB
        - ✅ Sistema human-in-the-loop
        - ✅ Avaliação de confiança
        """)
        
        st.subheader("📊 Dados Disponíveis")
        st.info("""
        **Banco de dados com 200 registros de cidades brasileiras:**
        - Cidades, estados e regiões
        - População
        - PIB total e per capita
        - Taxa de desemprego
        - Índice de educação
        """)
        
        st.subheader("💡 Exemplos de Perguntas")
        st.code("""
        • "Quais são as 10 cidades com maior PIB?"
        • "Analise a correlação entre população e PIB"
        • "Compare as regiões do Brasil"
        • "Busque informações sobre São Paulo"
        • "Gere insights sobre oportunidades de negócio"
        • "Lembre-se da última análise que fizemos"
        """)
        
        st.subheader("🎯 Tipos de Análise")
        
        analysis_types = {
            "📊 Análise de Dados": "Consultas estatísticas, rankings, métricas",
            "🔍 Busca e Filtros": "Busca por cidades, estados, regiões",
            "💡 Geração de Insights": "Análise de negócio, oportunidades, tendências",
            "📈 Análise de Correlação": "Relacionamentos entre variáveis",
            "🏛️ Análise Regional": "Comparações entre regiões do Brasil"
        }
        
        for analysis_type, description in analysis_types.items():
            st.write(f"**{analysis_type}:** {description}")

if __name__ == "__main__":
    main() 