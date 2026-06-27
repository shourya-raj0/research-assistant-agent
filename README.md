# Research Assistant Agent

An agentic AI system that autonomously researches topics, searches the web, and generates structured research summaries using LangGraph.

<<<<<<< HEAD
#Live Demo https://huggingface.co/spaces/shourya-raj/research-assistant-agent
=======
#Live Demo
https://huggingface.co/spaces/shourya-raj/research-assistant-agent
>>>>>>> 9499ef515f874a0c38f538cbdd2553982a994822

## Overview

This project demonstrates a multi-agent workflow built with LangGraph that:
- Refines user queries into optimized search terms
- Performs real-time web search using Tavily API
- Extracts key insights and generates structured summaries
- Returns validated JSON responses via FastAPI

## Architecture

User Query

↓

[Research Node] - Refine query using Groq LLM

↓

[Search Node] - Search web using Tavily API

↓

[Summarize Node] - Extract insights using Groq LLM

↓

Structured JSON Response

## 🛠️ Tech Stack

- **LangGraph** - Agent orchestration and workflow management
- **Groq** - Fast LLM inference 
- **Tavily** - Real-time web search
- **FastAPI** - REST API backend
- **Pydantic** - Data validation
- **Python 3.8+**

## 📋 Prerequisites

- Python 3.8 or higher
- Groq API key (free tier: https://console.groq.com)
- Tavily API key (free tier: https://tavily.com)

## 🚀 Installation

1. **Clone the repository:**
```bash
git clone https://github.com/shourya-raj0/research-assistant-agent.git
cd research-assistant-agent
```

2. **Create virtual environment:**
```bash
python -m venv venv
.\venv\Scripts\activate  # Windows
source venv/bin/activate  # macOS/Linux
```

3. **Install dependencies:**
```bash
pip install -r requirements.txt
```

4. **Set up environment variables:**
Create a `.env` file in the project root:


## 🔑 Key Features

✅ **Multi-Agent Architecture** - Specialized agents for each task
✅ **Stateful Workflow** - Shared state across all nodes
✅ **Real-time Web Search** - Uses Tavily for current information
✅ **Structured Output** - Validated JSON responses with Pydantic
✅ **Error Handling** - Graceful error management with status tracking
✅ **Fast LLM Inference** - Groq provides sub-second response times

## 📚 How It Works

1. **Research Node**: Takes raw user query and refines it into optimized search keywords using the Groq LLM
2. **Search Node**: Searches the web using Tavily API with the refined query
3. **Summarize Node**: Analyzes search results and extracts key insights, generating a structured summary

## 🎓 Learning Outcomes

Building this project demonstrates:
- LangGraph state management and workflow orchestration
- Multi-agent system design
- LLM prompt engineering
- FastAPI REST API development
- Tool integration (Tavily web search)
- Data validation with Pydantic
- Error handling in agentic systems

## 🚀 Future Enhancements

- [ ] LangSmith observability integration
- [ ] Multi-file document analysis
- [ ] GitHub repository research
- [ ] Custom knowledge base integration
- [ ] Deployment to Hugging Face Spaces


## 👤 Author

Shourya

Pull requests welcome! For major changes, please open an issue first.

---

**Built with ❤️ using LangGraph and Groq**
