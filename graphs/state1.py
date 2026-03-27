import os
from langgraph.graph import StateGraph,START,END
import operator
from langchain_core.prompts import ChatPromptTemplate
from typing import List, TypedDict,Annotated,Any
from langchain_core.messages import HumanMessage,BaseMessage,SystemMessage

class SchemaInfo(TypedDict):
    question:str
    all_tables:Annotated[List[str], operator.add]
    selected_tables:Annotated[List[str], operator.add]
    generated_sql: str
    is_safe: bool                   
    risk_level: str                 
    validation_issues: List[str]    
    needs_approval: bool
    execution_status: str            
    query_results: List[Any]         
    result_count: int                
    final_response: str
    error:str

