from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv
import os
from typing import List, Dict
import sys
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)
from database.connections import DatabaseManager
from config import DATABASE_URL
from utils.few_examples import format_examples_for_prompt

load_dotenv()

class SQLGenerator:
    def __init__(self):
        self.llm = ChatGroq(
            model="llama-3.1-8b-instant",
            groq_api_key=os.getenv("GROQ_API_KEY")
        )
        self.prompt = self.create_prompt()
    def create_prompt(self):
        template = """You are an expert SQL developer. Your task is to convert natural language questions into accurate SQL queries based on the provided database schema.

                     EXAMPLES OF QUESTION TO SQL CONVERSION:
                     {examples}
                     
                     DATABASE SCHEMA:
                     {schema}
                     
                     USER QUESTION:
                     {question}
                     
                     INSTRUCTIONS:
                     - Generate ONLY the SQL query, nothing else
                     - Do NOT include explanations or comments
                     - Do NOT use markdown code blocks (no ```sql)
                     - Ensure the query is syntactically correct for SQLite
                     - Use proper JOIN syntax when multiple tables are involved
                     - Use appropriate WHERE clauses for filtering
                     
                     SQL Query:"""
    
        return ChatPromptTemplate.from_template(template) 
    def _format_schema(self, schema: Dict) -> str:
        """
        Format schema dictionary into readable string
        
        Args:
            schema: Dict with table_name, columns, primary_keys, foreign_keys
            
        Returns:
            Formatted schema string
        """
        table_name=schema["table_name"]
        columns=[]
        for col in schema["columns"]:
            col_def=f"{col['name']} {col['type']}"
            if col['name'] in schema.get('primary_keys',[]):
                col_def+=" PRIMARY KEY"
            for fk in schema.get('foreign_keys', []):
              if col['name'] in fk.get('constrained_columns', []):
                ref_table = fk['referred_table']
                ref_col = fk['referred_columns'][0]
                col_def += f" REFERENCES {ref_table}({ref_col})"    
            columns.append(col_def)
        columns_str=", ".join(columns)
        formatted=f"{table_name}({columns_str})"
        return formatted
    def generate_sql(self, question: str, schemas: List[Dict]) -> str:
        """
        Generate SQL query from natural language question
        
        Args:
            question: User's natural language question
            schemas: List of schema dictionaries for selected tables
            
        Returns:
            Generated SQL query string
        """
        # TODO: Format all schemas
        formatted_schemas=[]
        for schema in schemas:
            formatted_schemas.append(self._format_schema(schema))
        all_schemas = "\n".join(formatted_schemas) 
        examples=format_examples_for_prompt()
        message=self.prompt.format_messages(
            examples=examples,
            schema=all_schemas,
            question=question

        )   
        
        response=self.llm.invoke(message)
        
        sql=response.content.strip()
        sql = sql.replace("```sql", "")
        sql = sql.replace("```", "")
        sql = sql.strip()

        return sql
       
def sql_generator_node(state: Dict) -> Dict:
    """
    LangGraph node function for SQL generation
    """
    try:
        # Extract from state
        question = state["question"]
        selected_tables = state["selected_tables"]
         # ✅ Add these lines
        current_file = os.path.abspath(__file__)
        agents_folder = os.path.dirname(current_file)
        project_root = os.path.dirname(agents_folder)
        db_path = os.path.join(project_root, "data", "my_database.db")
        db_url = f"sqlite:///{db_path}"
        
        print(f"DEBUG: Database path: {db_path}")  # For verification
        print(f"DEBUG: File exists: {os.path.exists(db_path)}")
        db_manager = DatabaseManager(db_url)
        
        schemas = []
        for table_name in selected_tables:
            schema = db_manager.get_table_schema(table_name)
            schema["table_name"] = table_name
            schemas.append(schema)
        
        # Generate SQL
        generator = SQLGenerator()
        generated_sql = generator.generate_sql(question, schemas)
        
        # Close connection
        db_manager.close()
        
        return {"generated_sql": generated_sql}
        
    except Exception as e:
        return {
            "generated_sql": "",
            "error": f"SQL generation failed: {str(e)}"
        }

if __name__ == "__main__":
    # Test the node function
    test_state = {
        "question": "Show customers from Delhi",
        "selected_tables": ["customers"],
        "all_tables": ["customers", "orders"],
        "generated_sql": "",
        "error": ""
    }
    
    result = sql_generator_node(test_state)
    print("Generated SQL:", result)