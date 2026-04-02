# 🤖 Intelligent Database Query Agent

An AI-powered system that converts natural language questions into SQL queries using LangGraph and LangChain.

## ✨ Features

- 🧠 **Natural Language to SQL** - Ask questions in plain English
- 🔍 **Smart Schema Selection** - Automatically identifies relevant tables
- 🤖 **AI-Powered SQL Generation** - Uses few-shot learning for accurate queries
- 🛡️ **Safety Validation** - Detects dangerous operations (DELETE, DROP, etc.)
- 👤 **Human-in-the-Loop** - Requires approval for risky queries
- ⚡ **Instant Execution** - Safe queries execute immediately
- 📊 **Formatted Results** - Clean, readable query results

## 🏗️ Architecture
```
User Question → Schema Selector → SQL Generator → Validator
                                                      ↓
                                                 Safe? ───Yes→ Execute → Results
                                                      ↓
                                                     No
                                                      ↓
                                            Human Approval
                                                ↓        ↓
                                            Approve  Reject
                                                ↓        ↓
                                            Execute   Block
```

## 🛠️ Tech Stack

- **LangGraph** - Agent orchestration and workflow management
- **LangChain** - LLM integration
- **Groq (Llama 3.1)** - Language model
- **SQLAlchemy** - Database operations
- **SQLite** - Database (easily adaptable to PostgreSQL/MySQL)

## 🚀 Quick Start

### Prerequisites
- Python 3.9+
- Groq API key

### Installation

1. Clone the repository:
```bash
git clone https://github.com/Abhay-Yadav1/intelligent-db-query-agent.git
cd intelligent-db-query-agent
```

2. Create virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create `.env` file:
```
GROQ_API_KEY=your_groq_api_key_here
DATABASE_URL=sqlite:///./data/my_database.db
ENVIRONMENT=development
```

5. Run the agent:
```bash
python main.py
```

## 💡 Usage Examples

### Safe Queries (Execute Immediately)
```
❓ Show all customers from Delhi
→ SELECT * FROM customers WHERE city = 'Delhi';
✅ Found 2 records

❓ Count total orders
→ SELECT COUNT(*) FROM orders;
✅ Found 1 record

❓ Show customer names with order count
→ SELECT c.name, COUNT(o.id) FROM customers c JOIN orders o...
✅ Found 3 records
```

### Risky Queries (Requires Approval)
```
❓ Delete customers from Mumbai

⚠️  APPROVAL REQUIRED
SQL: DELETE FROM customers WHERE city = 'Mumbai'
Risk Level: MEDIUM
Issues: Dangerous operation: DELETE

✋ Approve? (yes/no): no
❌ Query execution rejected
```

## 📁 Project Structure
```
intelligent-db-query-agent/
├── agents/               # AI agent implementations
│   ├── schema_selector.py
│   ├── sql_generator.py
│   ├── query_validator.py
│   ├── query_executor.py
│   └── human_approval.py
├── graphs/              # LangGraph workflows
│   ├── state1.py
│   └── complete_workflow.py
├── database/            # Database operations
│   ├── connections.py
│   └── setup_sample_db.py
├── utils/               # Utilities
│   └── few_examples.py
├── data/                # Database files
├── tests/               # Test files
├── main.py             # CLI entry point
└── README.md
```

## 🧪 Testing

Run tests:
```bash
python tests/test_complete_workflow.py
```

## 🎯 How It Works

1. **Schema Selector**: Identifies relevant database tables
2. **SQL Generator**: Creates SQL using few-shot learning
3. **Validator**: Checks query safety and assigns risk level
4. **Human Approval**: Pauses for approval if risky
5. **Executor**: Runs the query and formats results

## 🔒 Safety Features

- ✅ Keyword detection (DELETE, DROP, TRUNCATE, ALTER)
- ✅ Risk scoring (LOW/MEDIUM/HIGH)
- ✅ Syntax validation
- ✅ Human approval for dangerous operations
- ✅ Query rejection mechanism

## 📊 Project Stats

- **Lines of Code**: ~1000+
- **Agents**: 5 specialized agents
- **Development Time**: 9 days
- **Test Coverage**: 10+ test scenarios

## 🤝 Contributing

Feel free to open issues or submit pull requests!

## 📝 License

MIT License

## 👨‍💻 Author

Built by [Your Name] as a learning project in Agentic AI

---

**⭐ Star this repo if you found it useful!**
```

---

## **Task 4: Create requirements.txt - Final Version (2 mins)**

**File: `requirements.txt`**
```
langchain==0.1.0
langchain-openai==0.0.5
langchain-groq==0.0.1
langgraph==0.0.20
sqlalchemy==2.0.23
python-dotenv==1.0.0