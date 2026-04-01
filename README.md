# 🤖 Intelligent Database Query Agent

An AI-powered system that converts natural language questions into SQL queries using LangGraph and LangChain.

## 🎯 Project Overview

This project implements a multi-agent system that:
- Understands natural language questions about databases
- Generates safe and accurate SQL queries
- Validates queries for security and correctness
- Executes queries with human-in-the-loop approval for risky operations
- Learns from past queries to improve accuracy

## 🛠️ Tech Stack

- **LangGraph**: Agent orchestration and workflow management
- **LangChain**: LLM integration and chain building
- **SQLAlchemy**: Database connection and ORM
- **OpenAI GPT-4**: Language model for understanding and generation
- **SQLite**: Development database (easily adaptable to PostgreSQL/MySQL)

## 📁 Project Structure
```
intelligent-db-agent/
├── agents/          # Individual agent implementations
├── database/        # Database connection and utilities
├── graph/           # LangGraph workflow definitions
├── utils/           # Helper functions and utilities
├── data/            # Sample databases and examples
├── tests/           # Unit and integration tests
└── main.py          # Entry point
```

## 🚀 Getting Started

### Prerequisites
- Python 3.9+
- OpenAI API key

### Installation

1. Clone the repository:
```bash
git clone https://github.com/Abhay-Yadav1/intelligent-db-query-agent.git
cd intelligent-db-query-agent
```

2. Create virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create `.env` file:
```bash
OPENAI_API_KEY=your_api_key_here
DATABASE_URL=sqlite:///./data/sample_data.db
```



## 🎓 Learning Goals

This project is part of my journey to master:
- Agentic AI systems and orchestration
- LangGraph for complex workflows
- Production-ready AI applications
- Safe AI-database interactions




---

**Note**: This is an active learning project. Commits are made daily as I build and improve the system.
