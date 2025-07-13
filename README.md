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
<img width="656" height="522" alt="image" src="https://github.com/user-attachments/assets/b0ef5db0-d3ef-42cd-b5a6-32770b161557" />


## 🛠️ Features

- **Conversational Data Analysis:** Ask questions in plain English and get clear, well-formatted answers.
- **Comparative Insights:** Instantly compare cities, regions, or metrics.
- **Interactive Visualizations:** Bar charts, rankings, and trends—always sorted for clarity.
- **Robust Fallback:** Local analysis if the Grok API is unavailable.
- **Memory & History:** Review previous questions and answers.
- **Easy Setup:** No complex dependencies—just Python and a few libraries.

<img width="2838" height="1366" alt="image" src="https://github.com/user-attachments/assets/a90dde5f-6583-4724-9cce-beddef0c6d44" />
<img width="2814" height="1258" alt="image" src="https://github.com/user-attachments/assets/08dccc37-abaf-403a-bcde-b56b91774ee6" />
<img width="2832" height="1268" alt="image" src="https://github.com/user-attachments/assets/6435eec3-ddbe-47f5-8410-d5abe6641dd1" />
<img width="2536" height="1320" alt="image" src="https://github.com/user-attachments/assets/cbe76428-3415-4da3-b795-d281d9483d79" />
<img width="2770" height="1300" alt="image" src="https://github.com/user-attachments/assets/82f515e4-a8e3-4671-bd31-053ff068f532" />
<img width="2742" height="1318" alt="image" src="https://github.com/user-attachments/assets/ccb4960c-956b-4ee9-8ddc-010512989cb2" />
<img width="2790" height="1316" alt="image" src="https://github.com/user-attachments/assets/40d85cd9-23cc-4789-8e09-3beca823a2e4" />
<img width="1441" height="678" alt="image" src="https://github.com/user-attachments/assets/7abf6841-e448-4fcb-a4dc-0a1c6d10af34" />
<img width="2788" height="1362" alt="image" src="https://github.com/user-attachments/assets/cc3f5222-afa5-40b8-817b-53c3a4d45864" />
<img width="2094" height="1086" alt="image" src="https://github.com/user-attachments/assets/57698742-f95d-4f20-8856-f26169ca9e2b" />
<img width="2786" height="1370" alt="image" src="https://github.com/user-attachments/assets/fd03a1b3-bf9f-40d5-be0a-15301cc3e2b7" />
<img width="2800" height="1340" alt="image" src="https://github.com/user-attachments/assets/d503a03f-24ca-4908-b611-f38557dfc055" />


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

## 🔗 Useful Links

- [xAI Console](https://console.x.ai/)
- [Streamlit Documentation](https://docs.streamlit.io/)
- [DuckDB Documentation](https://duckdb.org/docs/)

---

LinkedIn: https://www.linkedin.com/in/alexsander-silveira-62b258200/
Medium: https://medium.com/@alexsander.silveira1

*Developed by Alexsander Silveira — empowering data-driven decisions in Brazil and beyond.*
