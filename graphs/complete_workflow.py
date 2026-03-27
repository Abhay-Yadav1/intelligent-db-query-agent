from langgraph.graph import StateGraph, START, END
from typing import Literal
import sys
import os

# Fix imports
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

from graphs.state1 import SchemaInfo
from agents.schema_selector import schema_selector_node
from agents.sql_generator import sql_generator_node
from agents.query_validator import query_validator_node
from agents.query_executor import query_executor_node
from agents.human_approval import human_approval_node

def create_complete_workflow():
    def should_request_approval(state: SchemaInfo) -> Literal["request_approval", "execute_query"]:
        if state.get("needs_approval", False):
            return "request_approval"
        else:
            return "execute_query"
   
    workflow = StateGraph(SchemaInfo)
 
    workflow.add_node("select_schema", schema_selector_node)
    workflow.add_node("generate_sql", sql_generator_node)
    workflow.add_node("validate_query", query_validator_node)
    workflow.add_node("request_approval", human_approval_node)
    workflow.add_node("execute_query", query_executor_node)
    workflow.add_edge(START, "select_schema")
    workflow.add_edge("select_schema", "generate_sql")
    workflow.add_edge("generate_sql", "validate_query")
    workflow.add_conditional_edges(
    "validate_query",
    should_request_approval,
    {
        "request_approval": "request_approval",
        "execute_query": "execute_query"
    }
    )
    workflow.add_edge("request_approval", "execute_query")
   
    workflow.add_edge("execute_query", END)
    app = workflow.compile()
    return app

if __name__ == "__main__":
    app = create_complete_workflow()
    
    # Test 1: Safe query (no approval needed)
    print("=== Test 1: Safe SELECT Query ===")
    result = app.invoke({
        "question": "Show all customers from New York",
        "all_tables": ["customers", "orders"],
        "selected_tables": [],
        "generated_sql": "",
        "is_safe": True,
        "risk_level": "LOW",
        "validation_issues": [],
        "needs_approval": False,
        "execution_status": "",
        "query_results": [],
        "result_count": 0,
        "final_response": "",
        "human_approved": None,
        "approval_message": "",
        "error": ""
    })
    
    print("Final Response:", result["final_response"])
    print("Results:", result["query_results"])