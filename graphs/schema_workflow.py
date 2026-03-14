import sys
import os
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

from langgraph.graph import StateGraph, START, END
from agents.schema_selector import schema_selector_node
from graphs.state1 import SchemaInfo

def create_schema_workflow():
    workflow=StateGraph(SchemaInfo)
    workflow.add_node("select_tables", schema_selector_node)
    workflow.add_edge(START, "select_tables")
    workflow.add_edge("select_tables", END)
    app=workflow.compile()
    return app

if __name__ == "__main__":
    app=create_schema_workflow()
    result = app.invoke({
        "question": "What is the total order value for each customer?",
        "all_tables": ["customers", "orders", "products"],
        "selected_tables": [],
        "error": ""
    })
    print(f"Question: {result['question']}")
    print(f"Selected tables: {result['selected_tables']}")
    print()
    
    # Test Case 3: Products only
    print("Test 3: Products query")
    result = app.invoke({
        "question": "List all available products",
        "all_tables": ["customers", "orders", "products"],
        "selected_tables": [],
        "error": ""
    })
    print(f"Question: {result['question']}")
    print(f"Selected tables: {result['selected_tables']}")
    print()

