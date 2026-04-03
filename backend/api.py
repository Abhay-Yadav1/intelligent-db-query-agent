from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.models import QueryRequest, QueryResponse
from backend.agent_service import agent_service

app = FastAPI(title="Intelligent DB Query Agent API")
# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # React app URL
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods (GET, POST, etc.)
    allow_headers=["*"],  # Allow all headers
)


@app.get("/")
def read_root():
    """Health check endpoint"""
    return {"status": "healthy", "message": "API is running"}

@app.post("/query", response_model=QueryResponse)
def query_database(request: QueryRequest):
    """
    Process a natural language database query
    """
    question=request.question
    result=agent_service.process_query(question)
    return QueryResponse(
        question=result.get("question", ""),
        sql=result.get("sql", ""),
        status=result.get("status", "error"),
        results=result.get("results", []),
        message=result.get("message", ""),
        error=result.get("error")
    )

@app.get("/tables")
def get_tables():
    """Get list of available database tables"""
    return {
        "tables": ["customers", "orders"]
    }