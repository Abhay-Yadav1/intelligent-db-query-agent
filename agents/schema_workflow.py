from langgraph.graph import StateGraph, START, END
from graphs.state1 import SchemaInfo
from agents.schema_selector import schema_selector_node

def create_schema_workflow():
    workflow=StateGraph(SchemaInfo)
    workflow.add_node("select_tables", schema_selector_node)
    workflow.add_edge(START, "select_tables")
    workflow.add_edge("select_tables", END)
    app=workflow.compile()
    return app



