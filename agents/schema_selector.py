import sys
import os
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)
from langchain_groq import ChatGroq
from dotenv import load_dotenv
import os
from langchain_core.prompts import ChatPromptTemplate
from typing import List, TypedDict,Annotated
from langchain_core.messages import HumanMessage,BaseMessage,SystemMessage
load_dotenv()

class SchemaSelector:
    def __init__(self):
        self.llm=ChatGroq(model="llama-3.1-8b-instant",
            groq_api_key=os.getenv("GROQ_API_KEY"))
        self.prompt=self.create_prompt()

    def create_prompt(self):
        """Create prompt template"""
        return ChatPromptTemplate.from_template(
            """You are a database expert. 
            
           Given these tables: {all_tables}
           User question: {question}

           Which tables are relevant? Return ONLY table names separated by commas.

            Relevant tables:"""
        )   
    def select_tables(self,question:str,all_tables:List[str])-> List[str]:
        messages=self.prompt.format_messages(
            question=question,
            all_tables=", ".join(all_tables)
        )
        response=self.llm.invoke(messages)
        result=response.content.strip()
        tables=[table.strip() for table in result.split(",") if table.strip() in all_tables]
        return tables
    
def schema_selector_node(state: dict) -> dict:
    """LangGraph node wrapper"""
    question = state["question"]
    all_tables = state["all_tables"]
    
    agent = SchemaSelector()
    selected = agent.select_tables(question, all_tables)
    
    return {"selected_tables": selected}    
if __name__ == "__main__":
    agent = SchemaSelector()
    
    result = agent.select_tables(
        question="Show me all customers from Delhi",
        all_tables=["customers", "orders", "products"]
    )
    
    print("Selected tables:", result)  



