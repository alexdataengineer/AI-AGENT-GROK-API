# 🤖 Intelligent Data Analysis Agent with Grok API

Hi! I'm Alexsander Silveira, and I developed this intelligent agent to deliver actionable insights about Brazilian cities using xAI's Grok API. This project is designed to empower professionals, researchers, and organizations to make data-driven decisions quickly and confidently.

---

## 🚀 Why This Project?

- **Democratize Data Intelligence:** Make advanced urban analytics accessible to everyone, not just data scientists.
- **Accelerate Decision-Making:** Instantly compare cities, spot opportunities, and understand regional trends.
- **Bridge Data and Action:** Turn raw data into clear, business-relevant insights for real-world impact.

## 🎯 Project Objective

To provide a robust, user-friendly platform for exploring, comparing, and understanding key metrics (population, GDP, unemployment, education) across 200 major Brazilian cities—powered by AI and ready for business, research, or public policy.

## 💡 Key Benefits & ROI

- **Faster Market Analysis:** Reduce research time from hours to seconds.
- **Better Decisions:** Data-backed recommendations for expansion, investment, or policy.
- **Cost Savings:** No need for expensive BI tools or custom dashboards.
- **Scalable:** Ready for new datasets, more cities, or other countries.
- **Security:** API keys and sensitive data are always protected.

## 🏗️ Architecture Overview

- **Grok API Integration:** Leverages xAI's Grok for natural language analysis and smart responses.
- **DuckDB Database:** Fast, in-memory analytics on local city data.
- **Decision Engine:** Confidence-based routing—uses Grok when possible, falls back to local logic if needed.
- **Memory System:** Remembers chat history and context for a more natural user experience.
- **Streamlit Web App:** Clean, interactive interface for chat, data visualization, and memory management.
- **Multilingual:** English and Portuguese support (easily extendable).
- **Secure Config:** API keys managed via environment variables, never hardcoded.
<img width="1024" height="1024" alt="image" src="https://github.com/user-attachments/assets/5a9737ff-b8dd-4085-9bc9-789043f7b1f0" />

## 🛠️ Features

- **Conversational Data Analysis:** Ask questions in plain English and get clear, well-formatted answers.
- **Comparative Insights:** Instantly compare cities, regions, or metrics.
- **Interactive Visualizations:** Bar charts, rankings, and trends—always sorted for clarity.
- **Robust Fallback:** Local analysis if the Grok API is unavailable.
- **Memory & History:** Review previous questions and answers.
- **Easy Setup:** No complex dependencies—just Python and a few libraries.

## 📋 Requirements

- Python 3.8+
- xAI account and Grok API key ([get yours here](https://console.x.ai/))

## ⚙️ Setup

1. **Clone the repository:**
   ```bash
   git clone <your-repo-url>
   cd AI-AGENT-GROK-API
   ```
2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
3. **Configure your API key:**
   - Copy the example file:
     ```bash
     cp .env.example .env
     ```
   - Edit `.env` and add your Grok API key:
     ```env
     XAI_API_KEY=your_grok_api_key_here
     XAI_API_URL=https://api.x.ai/v1/chat/completions
     ```

## 🚦 Usage

### Web Interface (Recommended)
```bash
# English version
python3 -m streamlit run agents/english/english_streamlit_app.py --server.port 8501

# Portuguese version
python3 -m streamlit run agents/portuguese/portuguese_streamlit_app.py --server.port 8502
```

### Command Line
```bash
python3 main.py
```

### API Test
```bash
python3 test_grok_api.py
```

## 📊 Example Questions

- "Compare São Paulo and Rio de Janeiro for tech investment."
- "What are the top 5 cities by GDP per capita?"
- "How is unemployment in the Northeast?"
- "Is Fortaleza a good city to live in?"
- "Show education index rankings for all regions."

## 🗂️ Project Structure

```
AI-AGENT-GROK-API/
├── agents/
│   ├── english/        # English version
│   └── portuguese/     # Portuguese version
├── data/               # City datasets
├── .env                # Your API key (never committed)
├── .env.example        # Template config
├── config.py           # System configuration
├── grok_api.py         # Grok API integration
├── data_manager.py     # Data management
├── memory_manager.py   # Memory system
├── decision_engine.py  # Decision engine
├── requirements.txt    # Dependencies
└── ...                 # Other modules
```

## 🛡️ Security

- API keys are always stored in `.env` (never in code)
- `.env` is in `.gitignore` by default
- Configuration is validated at startup
- Local fallback ensures no data loss if API fails

## 🛠️ Troubleshooting

- **API key not found:**
  - Make sure `.env` exists and contains your key
  - Never commit `.env` to GitHub
- **API not responding:**
  - Check your internet connection
  - Verify your API key is correct
  - The system will use local fallback if needed
- **Port already in use:**
  - Use a different port, e.g. `--server.port 8503`

## 🤝 Contribution

1. Fork this project
2. Create a feature branch
3. Commit your changes
4. Push to your branch
5. Open a Pull Request

## 📄 License

MIT License. See [LICENSE](LICENSE) for details.

## 🔗 Useful Links

- [xAI Console](https://console.x.ai/)
- [Streamlit Documentation](https://docs.streamlit.io/)
- [DuckDB Documentation](https://duckdb.org/docs/)

---

**⚠️ IMPORTANT:** Never commit your `.env` file or API keys to any public repository.

---

*Developed by Alexsander Silveira — empowering data-driven decisions in Brazil and beyond.*
