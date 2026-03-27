from langgraph.graph import StateGraph, START, END
from typing import Literal
import sys
import os
from langgraph.checkpoint.memory import MemorySaver
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
    memory = MemorySaver()
    app = workflow.compile(
        checkpointer=memory,
        interrupt_before=["execute_query"]  # Pause before execution if approval needed
    )
    return app

if __name__ == "__main__":
    app = create_complete_workflow()
    
    # Test 2: Risky query (needs approval)
    print("=== Test 2: DELETE Query (Needs Approval) ===")
    
    config = {"configurable": {"thread_id": "test-thread-1"}}
    
    # Initial run - will pause at approval
    result = app.invoke({
        "question": "Show all customer named",
        "all_tables": ["customers", "orders"],
        "selected_tables": [],
        # ... (rest of initial state)
    }, config)
    
    print("Paused for approval")
    print("Approval Message:", result.get("approval_message"))
    
    # Simulate human approval
    print("\n--- Human approves ---")
    
    # Update state with approval
    app.update_state(
        config,
        {"human_approved": True, "is_safe": True}
    )
    
    # Resume execution
    final_result = app.invoke(None, config)
    
    print("Final Response:", final_result["final_response"])