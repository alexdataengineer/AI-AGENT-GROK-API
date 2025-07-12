#!/usr/bin/env python3
"""
English Streamlit App for Intelligent Data Analysis Agent
- Enhanced UI/UX
- Real-time data visualization
- Memory management
- Business insights dashboard
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import json
import requests
from typing import Dict, List, Any, Optional

# Import our agent
from english_agent import EnglishDataAnalysisAgent

# Page configuration
st.set_page_config(
    page_title="Intelligent Data Analysis Agent",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #1f77b4;
    }
    .success-message {
        background-color: #d4edda;
        color: #155724;
        padding: 1rem;
        border-radius: 0.5rem;
        border: 1px solid #c3e6cb;
    }
    .info-message {
        background-color: #d1ecf1;
        color: #0c5460;
        padding: 1rem;
        border-radius: 0.5rem;
        border: 1px solid #bee5eb;
    }
    .warning-message {
        background-color: #fff3cd;
        color: #856404;
        padding: 1rem;
        border-radius: 0.5rem;
        border: 1px solid #ffeaa7;
    }
</style>
""", unsafe_allow_html=True)

class EnglishStreamlitApp:
    def __init__(self):
        """Initialize the Streamlit application"""
        self.agent = EnglishDataAnalysisAgent()
        self.initialize_session_state()
    
    def initialize_session_state(self):
        """Initialize session state variables"""
        if 'chat_history' not in st.session_state:
            st.session_state.chat_history = []
        if 'memory_summary' not in st.session_state:
            st.session_state.memory_summary = {}
        if 'data_overview' not in st.session_state:
            st.session_state.data_overview = {}
    
    def render_header(self):
        """Render the main header"""
        st.markdown("""
        <div style="text-align: center; padding: 2rem; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; border-radius: 1rem; margin-bottom: 2rem;">
            <h1 style="margin: 0; font-size: 2.5rem; font-weight: bold;">🤖 Intelligent Data Analysis Agent</h1>
            <p style="margin: 0.5rem 0 0 0; font-size: 1.2rem; opacity: 0.9;">Brazilian Cities Economic Analysis & Business Intelligence</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Status indicators in a clean card layout
        with st.container():
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                if self.agent.grok_api.connected:
                    st.markdown("""
                    <div style="background-color: #d4edda; padding: 1rem; border-radius: 0.5rem; text-align: center; border: 1px solid #c3e6cb;">
                        <h4 style="margin: 0; color: #155724;">✅ Grok API</h4>
                        <p style="margin: 0; color: #155724; font-size: 0.9rem;">Connected</p>
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown("""
                    <div style="background-color: #fff3cd; padding: 1rem; border-radius: 0.5rem; text-align: center; border: 1px solid #ffeaa7;">
                        <h4 style="margin: 0; color: #856404;">⚠️ Local Mode</h4>
                        <p style="margin: 0; color: #856404; font-size: 0.9rem;">Offline</p>
                    </div>
                    """, unsafe_allow_html=True)
            
            with col2:
                st.markdown("""
                <div style="background-color: #d1ecf1; padding: 1rem; border-radius: 0.5rem; text-align: center; border: 1px solid #bee5eb;">
                    <h4 style="margin: 0; color: #0c5460;">📊 Data</h4>
                    <p style="margin: 0; color: #0c5460; font-size: 0.9rem;">200 Cities</p>
                </div>
                """, unsafe_allow_html=True)
            
            with col3:
                st.markdown("""
                <div style="background-color: #e2e3e5; padding: 1rem; border-radius: 0.5rem; text-align: center; border: 1px solid #d6d8db;">
                    <h4 style="margin: 0; color: #383d41;">🧠 Memory</h4>
                    <p style="margin: 0; color: #383d41; font-size: 0.9rem;">Active</p>
                </div>
                """, unsafe_allow_html=True)
            
            with col4:
                st.markdown("""
                <div style="background-color: #f8d7da; padding: 1rem; border-radius: 0.5rem; text-align: center; border: 1px solid #f5c6cb;">
                    <h4 style="margin: 0; color: #721c24;">🔄 Analysis</h4>
                    <p style="margin: 0; color: #721c24; font-size: 0.9rem;">Real-time</p>
                </div>
                """, unsafe_allow_html=True)
    
    def render_sidebar(self):
        """Render the sidebar with controls"""
        st.sidebar.title("🎛️ Control Panel")
        
        # Agent status
        st.sidebar.markdown("### Agent Status")
        if self.agent.grok_api.connected:
            st.sidebar.success("Grok API: Connected")
        else:
            st.sidebar.warning("Grok API: Offline")
        
        # Memory management
        st.sidebar.markdown("### Memory Management")
        if st.sidebar.button("📊 View Memory Summary", key="sidebar_view_memory"):
            self.show_memory_summary()
        
        if st.sidebar.button("🗑️ Clear Memory", key="sidebar_clear_memory"):
            self.agent.clear_memory()
            st.sidebar.success("Memory cleared!")
        
        if st.sidebar.button("💾 Export Memory", key="sidebar_export_memory"):
            if self.agent.export_memory("memory_export.json"):
                st.sidebar.success("Memory exported!")
            else:
                st.sidebar.error("Export failed!")
        
        # Data overview
        st.sidebar.markdown("### Data Overview")
        data_overview = self.agent.get_data_overview()
        
        st.sidebar.metric("Total Records", f"{data_overview['total_records']:,}")
        st.sidebar.metric("Cities", data_overview['total_cities'])
        st.sidebar.metric("States", data_overview['total_states'])
        st.sidebar.metric("Regions", data_overview['total_regions'])
        
        # Quick actions
        st.sidebar.markdown("### Quick Actions")
        if st.sidebar.button("🏆 Top 10 Cities", key="sidebar_top_cities"):
            self.show_top_cities()
        
        if st.sidebar.button("📈 Regional Analysis", key="sidebar_regional_analysis"):
            self.show_regional_analysis()
        
        if st.sidebar.button("💡 Business Insights", key="sidebar_business_insights"):
            self.show_business_insights()
    
    def render_chat_interface(self):
        """Render the main chat interface"""
        st.markdown("## 💬 Ask Questions About Brazilian Cities")
        
        # Create a clean input area
        with st.container():
            st.markdown("""
            <div style="background-color: #f8f9fa; padding: 1.5rem; border-radius: 0.5rem; border: 1px solid #dee2e6;">
                <h4 style="margin-bottom: 1rem;">🤖 Intelligent Data Analysis</h4>
            </div>
            """, unsafe_allow_html=True)
            
            # Chat input with better styling
            user_input = st.text_input(
                "💭 Enter your question:",
                placeholder="e.g., What's São Paulo's GDP? Compare São Paulo vs Belo Horizonte...",
                key="user_input"
            )
            
            col1, col2, col3 = st.columns([1, 1, 2])
            
            with col1:
                if st.button("🚀 Analyze", type="primary", key="analyze_btn", use_container_width=True):
                    if user_input.strip():
                        self.process_user_question(user_input)
            
            with col2:
                if st.button("🎲 Examples", key="example_questions_btn", use_container_width=True):
                    self.show_example_questions()
            
            with col3:
                st.markdown("<small>💡 Try questions about cities, GDP, comparisons, or business insights</small>", unsafe_allow_html=True)
        
        # Display chat history in a cleaner format
        if st.session_state.chat_history:
            st.markdown("---")
            st.markdown("## 📝 Conversation History")
            
            for i, (question, response, confidence, timestamp) in enumerate(st.session_state.chat_history):
                with st.expander(f"💬 Q{i+1}: {question[:60]}...", expanded=False):
                    # Question section
                    st.markdown("""
                    <div style="background-color: #e3f2fd; padding: 1rem; border-radius: 0.5rem; margin-bottom: 1rem;">
                        <h5 style="margin: 0; color: #1976d2;">❓ Question</h5>
                        <p style="margin: 0.5rem 0 0 0;">{}</p>
                        <small style="color: #666;">Confidence: {:.2f} | Time: {}</small>
                    </div>
                    """.format(question, confidence, timestamp), unsafe_allow_html=True)
                    
                    # Response section
                    st.markdown("""
                    <div style="background-color: #f3e5f5; padding: 1rem; border-radius: 0.5rem;">
                        <h5 style="margin: 0; color: #7b1fa2;">💡 Response</h5>
                        <div style="margin-top: 0.5rem;">
                    """, unsafe_allow_html=True)
                    
                                # Format response sections
            if response and isinstance(response, str):
                response_sections = response.split('\n\n')
                for section in response_sections:
                    if section.strip():
                        st.markdown(section)
                        st.markdown("")  # Add spacing
            else:
                st.error("❌ Error: No response received from the agent")
            
            st.markdown("</div></div>", unsafe_allow_html=True)
    
    def process_user_question(self, question: str):
        """Process user question and display response"""
        with st.spinner("🤖 Analyzing your question..."):
            try:
                result = self.agent.process_user_input(question)
                
                # Validate result
                if not result or not isinstance(result, dict):
                    st.error("❌ Error: Invalid response from agent")
                    return
                
                # Ensure response exists
                if 'response' not in result or not result['response']:
                    st.error("❌ Error: No response received from agent")
                    return
                
                # Add to chat history
                st.session_state.chat_history.append((
                    question,
                    result['response'],
                    result.get('confidence', 0.0),
                    datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                ))
                
                # Display results
                self.display_analysis_results(result)
                
            except Exception as e:
                st.error(f"❌ Error processing question: {str(e)}")
                st.info("💡 Try asking a simpler question or check your internet connection")
    
    def display_analysis_results(self, result: Dict[str, Any]):
        """Display analysis results in a structured way"""
        
        # Validate result data
        if not result or not isinstance(result, dict):
            st.error("❌ Error: Invalid result data")
            return
        
        # Create a clean header
        st.markdown("---")
        st.markdown("## 📊 Analysis Results")
        
        # Metrics in a clean card layout
        with st.container():
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                confidence = result.get('confidence', 0.0)
                st.markdown("""
                <div style="background-color: #f0f2f6; padding: 0.5rem; border-radius: 0.5rem; border-left: 4px solid #1f77b4;">
                    <h6 style="margin: 0; color: #1f77b4; font-size: 0.8rem;">Confidence</h6>
                    <h4 style="margin: 0; color: #1f77b4;">{:.2f}</h4>
                </div>
                """.format(confidence), unsafe_allow_html=True)
            
            with col2:
                decision_type = result.get('decision_type', 'unknown').replace('_', ' ').title()
                st.markdown("""
                <div style="background-color: #f0f2f6; padding: 0.5rem; border-radius: 0.5rem; border-left: 4px solid #28a745;">
                    <h6 style="margin: 0; color: #28a745; font-size: 0.8rem;">Decision Type</h6>
                    <h4 style="margin: 0; color: #28a745; font-size: 0.9rem;">{}</h4>
                </div>
                """.format(decision_type), unsafe_allow_html=True)
            
            with col3:
                quality_metrics = result.get('quality_metrics', {})
                quality_score = quality_metrics.get('overall_score', 0.0)
                st.markdown("""
                <div style="background-color: #f0f2f6; padding: 0.5rem; border-radius: 0.5rem; border-left: 4px solid #ffc107;">
                    <h6 style="margin: 0; color: #ffc107; font-size: 0.8rem;">Quality Score</h6>
                    <h4 style="margin: 0; color: #ffc107;">{:.2f}</h4>
                </div>
                """.format(quality_score), unsafe_allow_html=True)
            
            with col4:
                if result.get('needs_human_help'):
                    st.markdown("""
                    <div style="background-color: #fff3cd; padding: 0.5rem; border-radius: 0.5rem; border-left: 4px solid #ffc107;">
                        <h6 style="margin: 0; color: #856404; font-size: 0.8rem;">Status</h6>
                        <h4 style="margin: 0; color: #856404;">🤔 Human Help</h4>
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown("""
                    <div style="background-color: #d4edda; padding: 0.5rem; border-radius: 0.5rem; border-left: 4px solid #28a745;">
                        <h6 style="margin: 0; color: #155724; font-size: 0.8rem;">Status</h6>
                        <h4 style="margin: 0; color: #155724;">✅ Complete</h4>
                    </div>
                    """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Display response in a clean format
        st.markdown("## 💡 Analysis Response")
        
        if result.get('needs_human_help'):
            st.warning(result['response'])
        else:
            # Format the response with better styling
            response_text = result['response']
            
            # Split into sections for better readability
            sections = response_text.split('\n\n')
            
            for i, section in enumerate(sections):
                if section.strip():
                    if section.startswith('###'):
                        # Headers
                        st.markdown(section)
                    elif section.startswith('- **') or section.startswith('• **'):
                        # Lists with bold items
                        st.markdown(section)
                    elif '**' in section and ':' in section:
                        # Key-value pairs
                        st.markdown(section)
                    else:
                        # Regular paragraphs
                        st.markdown(section)
                    
                    if i < len(sections) - 1:
                        st.markdown("")  # Add spacing between sections
        
        # Show data used in a subtle way
        if result.get('data_used'):
            st.markdown("---")
            st.markdown(f"<small>📊 <em>Data source: {result['data_used']}</em></small>", unsafe_allow_html=True)
    
    def show_example_questions(self):
        """Show example questions"""
        examples = [
            "What are the top 10 cities by GDP?",
            "Compare São Paulo vs Belo Horizonte for business investment",
            "Which cities are best for retail expansion?",
            "Analyze the correlation between population and GDP",
            "What are the economic opportunities in the Northeast region?",
            "Generate business insights for tech startups",
            "Compare Brazilian regions by economic indicators",
            "What's the best city for manufacturing investment?"
        ]
        
        st.markdown("### 💡 Example Questions")
        for i, example in enumerate(examples, 1):
            st.markdown(f"{i}. {example}")
    
    def show_memory_summary(self):
        """Show memory summary"""
        memory_summary = self.agent.get_memory_summary()
        
        st.markdown("### 🧠 Memory Summary")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Total Interactions", memory_summary.get('total_interactions', 0))
        
        with col2:
            avg_confidence = memory_summary.get('average_confidence', 0)
            st.metric("Average Confidence", f"{avg_confidence:.2f}")
        
        with col3:
            min_confidence = memory_summary.get('min_confidence', 0)
            st.metric("Min Confidence", f"{min_confidence:.2f}")
        
        with col4:
            max_confidence = memory_summary.get('max_confidence', 0)
            st.metric("Max Confidence", f"{max_confidence:.2f}")
    
    def show_top_cities(self):
        """Show top cities visualization"""
        st.markdown("### 🏆 Top 10 Cities by GDP")
        
        # Get top cities data
        top_cities = self.agent.data_manager.get_top_cities("gdp_total", 10)
        
        if top_cities:
            # Create DataFrame
            df = pd.DataFrame(top_cities)
            
            # Sort data from highest to lowest
            df_sorted = df.sort_values('gdp_total', ascending=False)
            
            # Create visualization
            fig = px.bar(
                df_sorted,
                x='city',
                y='gdp_total',
                title="Top 10 Cities by GDP (R$ billions) - Ordered by Highest to Lowest",
                labels={'gdp_total': 'GDP (R$ billions)', 'city': 'City'},
                color='gdp_total',
                color_continuous_scale='viridis'
            )
            
            fig.update_layout(
                xaxis_tickangle=-45,
                height=500,
                xaxis={'categoryorder': 'total descending'}
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
            # Show detailed table
            st.markdown("### 📋 Detailed Data")
            
            # Format GDP for display
            display_df = df.copy()
            display_df['gdp_total_formatted'] = display_df['gdp_total'].apply(
                lambda x: f"R$ {x/1e9:.1f}B"
            )
            display_df['gdp_per_capita_formatted'] = display_df['gdp_per_capita'].apply(
                lambda x: f"R$ {x:,.0f}"
            )
            
            st.dataframe(
                display_df[['city', 'state', 'region', 'gdp_total_formatted', 
                           'gdp_per_capita_formatted', 'unemployment_rate', 'education_index']],
                use_container_width=True
            )
    
    def show_regional_analysis(self):
        """Show regional analysis"""
        st.markdown("### 📈 Regional Economic Analysis")
        
        # Get regional data
        regional_data = self.agent.data_manager.analyze_by_region()
        
        if regional_data:
            # Create DataFrame
            df = pd.DataFrame(regional_data)
            
            # Sort data by GDP per capita (highest to lowest)
            df_sorted = df.sort_values('avg_gdp_per_capita', ascending=False)
            
            # Create visualization
            fig = px.scatter(
                df_sorted,
                x='avg_gdp_per_capita',
                y='avg_unemployment_rate',
                size='total_population',
                color='region',
                title="Regional Analysis: GDP per Capita vs Unemployment Rate - Ordered by Highest GDP per Capita",
                labels={
                    'avg_gdp_per_capita': 'Average GDP per Capita (R$)',
                    'avg_unemployment_rate': 'Average Unemployment Rate (%)',
                    'total_population': 'Total Population'
                }
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
            # Show regional table
            st.markdown("### 📊 Regional Data")
            
            display_df = df.copy()
            display_df['total_population_formatted'] = display_df['total_population'].apply(
                lambda x: f"{x:,.0f}"
            )
            display_df['total_gdp_region_formatted'] = display_df['total_gdp_region'].apply(
                lambda x: f"R$ {x/1e9:.1f}B"
            )
            display_df['avg_gdp_per_capita_formatted'] = display_df['avg_gdp_per_capita'].apply(
                lambda x: f"R$ {x:,.0f}"
            )
            
            st.dataframe(
                display_df[['region', 'num_cities', 'total_population_formatted',
                           'total_gdp_region_formatted', 'avg_gdp_per_capita_formatted',
                           'avg_unemployment_rate']],
                use_container_width=True
            )
    
    def show_business_insights(self):
        """Show business insights dashboard"""
        st.markdown("### 💼 Business Intelligence Dashboard")
        
        # Get data for insights
        cities_data = self.agent.data_manager.cities_data
        df = pd.DataFrame(cities_data)
        
        # Create multiple visualizations
        col1, col2 = st.columns(2)
        
        with col1:
            # GDP vs Population correlation
            fig1 = px.scatter(
                df,
                x='population',
                y='gdp_total',
                color='region',
                title="GDP vs Population Correlation",
                labels={'population': 'Population', 'gdp_total': 'GDP (R$)'}
            )
            st.plotly_chart(fig1, use_container_width=True)
        
        with col2:
            # Unemployment vs Education
            fig2 = px.scatter(
                df,
                x='education_index',
                y='unemployment_rate',
                color='region',
                title="Education Index vs Unemployment Rate",
                labels={'education_index': 'Education Index', 'unemployment_rate': 'Unemployment Rate (%)'}
            )
            st.plotly_chart(fig2, use_container_width=True)
        
        # Business insights text
        st.markdown("### 💡 Key Business Insights")
        
        insights = [
            "🏙️ **São Paulo** leads with R$ 748.8B GDP - ideal for large-scale operations",
            "💰 **Brasília** has highest GDP per capita (R$ 83,250) - premium market opportunities",
            "🎓 **São Paulo** has highest education index (0.87) - qualified workforce",
            "📈 **South region** shows lowest unemployment rates - stable business environment",
            "🌅 **Northeast** offers growth potential with lower competition and costs"
        ]
        
        for insight in insights:
            st.markdown(f"• {insight}")
    
    def render_data_visualization_tab(self):
        """Render data visualization tab"""
        st.markdown("### 📊 Data Visualization")
        
        # Get cities data
        cities_data = self.agent.data_manager.cities_data
        df = pd.DataFrame(cities_data)
        
        # Create visualizations
        tab1, tab2, tab3, tab4 = st.tabs(["GDP Analysis", "Demographics", "Economic Indicators", "Regional Comparison"])
        
        with tab1:
            st.markdown("#### 💰 GDP Analysis")
            
            col1, col2 = st.columns(2)
            
            with col1:
                # GDP Total - Ordered from highest to lowest
                df_gdp_sorted = df.sort_values('gdp_total', ascending=False).head(10)
                fig_gdp = px.bar(
                    df_gdp_sorted,
                    x='city',
                    y='gdp_total',
                    title="Top 10 Cities by Total GDP - Ordered by Highest to Lowest",
                    labels={'gdp_total': 'GDP (R$ billions)', 'city': 'City'}
                )
                fig_gdp.update_layout(
                    xaxis_tickangle=-45,
                    xaxis={'categoryorder': 'total descending'}
                )
                st.plotly_chart(fig_gdp, use_container_width=True)
            
            with col2:
                # GDP per Capita - Ordered from highest to lowest
                df_capita_sorted = df.sort_values('gdp_per_capita', ascending=False).head(10)
                fig_gdp_capita = px.bar(
                    df_capita_sorted,
                    x='city',
                    y='gdp_per_capita',
                    title="Top 10 Cities by GDP per Capita - Ordered by Highest to Lowest",
                    labels={'gdp_per_capita': 'GDP per Capita (R$)', 'city': 'City'}
                )
                fig_gdp_capita.update_layout(
                    xaxis_tickangle=-45,
                    xaxis={'categoryorder': 'total descending'}
                )
                st.plotly_chart(fig_gdp_capita, use_container_width=True)
        
        with tab2:
            st.markdown("#### 👥 Demographics")
            
            col1, col2 = st.columns(2)
            
            with col1:
                # Population - Ordered from highest to lowest
                df_pop_sorted = df.sort_values('population', ascending=False).head(10)
                fig_pop = px.bar(
                    df_pop_sorted,
                    x='city',
                    y='population',
                    title="Top 10 Cities by Population - Ordered by Highest to Lowest",
                    labels={'population': 'Population', 'city': 'City'}
                )
                fig_pop.update_layout(
                    xaxis_tickangle=-45,
                    xaxis={'categoryorder': 'total descending'}
                )
                st.plotly_chart(fig_pop, use_container_width=True)
            
            with col2:
                # Population by Region - Ordered from highest to lowest
                region_pop = df.groupby('region')['population'].sum().reset_index()
                region_pop_sorted = region_pop.sort_values('population', ascending=False)
                fig_pop_region = px.bar(
                    region_pop_sorted,
                    x='region',
                    y='population',
                    title="Population by Region - Ordered by Highest to Lowest",
                    labels={'population': 'Population', 'region': 'Region'}
                )
                fig_pop_region.update_layout(
                    xaxis={'categoryorder': 'total descending'}
                )
                st.plotly_chart(fig_pop_region, use_container_width=True)
        
        with tab3:
            st.markdown("#### 📈 Economic Indicators")
            
            col1, col2 = st.columns(2)
            
            with col1:
                # Unemployment Rate - Ordered from lowest to highest (best to worst)
                df_unemployment_sorted = df.sort_values('unemployment_rate', ascending=True)
                fig_unemployment = px.bar(
                    df_unemployment_sorted,
                    x='city',
                    y='unemployment_rate',
                    title="Unemployment Rate by City - Ordered from Lowest to Highest",
                    labels={'unemployment_rate': 'Unemployment Rate (%)', 'city': 'City'}
                )
                fig_unemployment.update_layout(
                    xaxis_tickangle=-45,
                    xaxis={'categoryorder': 'total ascending'}
                )
                st.plotly_chart(fig_unemployment, use_container_width=True)
            
            with col2:
                # Education Index - Ordered from highest to lowest (best to worst)
                df_education_sorted = df.sort_values('education_index', ascending=False)
                fig_education = px.bar(
                    df_education_sorted,
                    x='city',
                    y='education_index',
                    title="Education Index by City - Ordered from Highest to Lowest",
                    labels={'education_index': 'Education Index', 'city': 'City'}
                )
                fig_education.update_layout(
                    xaxis_tickangle=-45,
                    xaxis={'categoryorder': 'total descending'}
                )
                st.plotly_chart(fig_education, use_container_width=True)
        
        with tab4:
            st.markdown("#### 🗺️ Regional Comparison")
            
            # Regional summary
            regional_summary = df.groupby('region').agg({
                'gdp_total': 'sum',
                'population': 'sum',
                'unemployment_rate': 'mean',
                'education_index': 'mean'
            }).reset_index()
            
            fig_region = px.scatter(
                regional_summary,
                x='gdp_total',
                y='population',
                size='education_index',
                color='region',
                title="Regional Economic Overview",
                labels={
                    'gdp_total': 'Total GDP (R$)',
                    'population': 'Population',
                    'education_index': 'Education Index'
                }
            )
            st.plotly_chart(fig_region, use_container_width=True)
    
    def render_memory_tab(self):
        """Render memory management tab"""
        st.markdown("### 🧠 Memory Management")
        
        # Memory summary
        memory_summary = self.agent.get_memory_summary()
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Total Interactions", memory_summary.get('total_interactions', 0))
        
        with col2:
            avg_conf = memory_summary.get('average_confidence', 0)
            st.metric("Average Confidence", f"{avg_conf:.2f}")
        
        with col3:
            min_conf = memory_summary.get('min_confidence', 0)
            st.metric("Min Confidence", f"{min_conf:.2f}")
        
        with col4:
            max_conf = memory_summary.get('max_confidence', 0)
            st.metric("Max Confidence", f"{max_conf:.2f}")
        
        # Memory actions
        st.markdown("#### 🔧 Memory Actions")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("🗑️ Clear All Memory", key="clear_memory_btn"):
                self.agent.clear_memory()
                st.success("Memory cleared successfully!")
        
        with col2:
            if st.button("💾 Export Memory", key="export_memory_btn"):
                if self.agent.export_memory("memory_export.json"):
                    st.success("Memory exported to 'memory_export.json'")
                else:
                    st.error("Export failed!")
        
        with col3:
            if st.button("📊 Memory Analytics", key="memory_analytics_btn"):
                self.show_memory_analytics()
        
        # Recent interactions
        if st.session_state.chat_history:
            st.markdown("#### 📝 Recent Interactions")
            
            for i, (question, response, confidence, timestamp) in enumerate(st.session_state.chat_history[-5:], 1):
                with st.expander(f"Interaction {i}: {question[:50]}...", expanded=False):
                    st.markdown(f"**Question:** {question}")
                    st.markdown(f"**Confidence:** {confidence:.2f}")
                    st.markdown(f"**Timestamp:** {timestamp}")
                    st.markdown("**Response:**")
                    st.markdown(response[:200] + "..." if len(response) > 200 else response)
    
    def show_memory_analytics(self):
        """Show memory analytics"""
        st.markdown("#### 📊 Memory Analytics")
        
        if st.session_state.chat_history:
            # Create analytics
            confidences = [conf for _, _, conf, _ in st.session_state.chat_history]
            
            col1, col2 = st.columns(2)
            
            with col1:
                # Confidence distribution
                fig_conf = px.histogram(
                    x=confidences,
                    title="Confidence Distribution",
                    labels={'x': 'Confidence Level', 'y': 'Frequency'}
                )
                st.plotly_chart(fig_conf, use_container_width=True)
            
            with col2:
                # Confidence over time
                timestamps = [ts for _, _, _, ts in st.session_state.chat_history]
                fig_time = px.line(
                    x=range(len(confidences)),
                    y=confidences,
                    title="Confidence Over Time",
                    labels={'x': 'Interaction Number', 'y': 'Confidence Level'}
                )
                st.plotly_chart(fig_time, use_container_width=True)
        else:
            st.info("No memory data available for analytics.")

def main():
    """Main function to run the Streamlit app"""
    app = EnglishStreamlitApp()
    
    # Render header
    app.render_header()
    
    # Render sidebar
    app.render_sidebar()
    
    # Create tabs
    tab1, tab2, tab3 = st.tabs(["💬 Chat Interface", "📊 Data Visualization", "🧠 Memory Management"])
    
    with tab1:
        app.render_chat_interface()
    
    with tab2:
        app.render_data_visualization_tab()
    
    with tab3:
        app.render_memory_tab()

if __name__ == "__main__":
    main() 