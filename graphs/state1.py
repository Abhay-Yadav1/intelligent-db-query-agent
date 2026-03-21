import os
from langgraph.graph import StateGraph,START,END
import operator
from langchain_core.prompts import ChatPromptTemplate
from typing import List, TypedDict,Annotated
from langchain_core.messages import HumanMessage,BaseMessage,SystemMessage

class SchemaInfo(TypedDict):
    question:str
    all_tables:Annotated[List[str], operator.add]
    selected_tables:Annotated[List[str], operator.add]
    generated_sql: str
    error:str

