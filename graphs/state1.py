from langchain_groq import ChatGroq
from dotenv import load_dotenv
import os
from langgraph.graph import StateGraph,START,END
import operator
from langchain_core.prompts import ChatPromptTemplate
from typing import List, TypedDict,Annotated
from langchain_core.messages import HumanMessage,BaseMessage,SystemMessage

class SchemaInfo(TypedDict):
    question:str
    all_table_names:Annotated[List[str], operator.add]
    relavent_table_names:Annotated[List[str], operator.add]
    error:str

    