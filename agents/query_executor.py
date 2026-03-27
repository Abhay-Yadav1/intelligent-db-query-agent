from typing import Dict, List, Any
import sys
import os

project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

from database.connections import DatabaseManager
from config import DATABASE_URL
class QueryExecutor:
    def __init__(self, db_url: str):
       
        self.db_manager=DatabaseManager(db_url)
        
    
    def execute_query(self, sql: str, is_safe: bool = True) -> Dict:
        if not is_safe:
           return {
            "execution_status": "blocked",
            "results": [],
            "row_count": 0,
            "error_message": "Query blocked - not validated as safe",
            "formatted_response": "Query execution blocked for safety reasons"
        }
        try:
            raw_results=self.db_manager.execute_query(sql)
            formatted = self._format_results(raw_results, sql)
            return formatted
        
        except Exception as e:
          return {
            "execution_status": "error",
            "results": [],
            "row_count": 0,
            "error_message": str(e),
            "formatted_response": f"Query execution failed: {str(e)}"
        }
        
    
    def _format_results(self, raw_results: Any, sql: str) -> Dict:
        sql_upper=sql.strip().upper()
        if sql_upper.startswith('SELECT'):
            results=[]
            if raw_results:
                if isinstance(raw_results,list):
                    results=[list(row) for row in raw_results]
            row_count=len(results)
            message=self._create_response_message(results,sql)
            return {
            "execution_status": "success",
            "results": results,
            "row_count": row_count,
            "formatted_response": message
            } 
        else:
            affected_rows = raw_results if isinstance(raw_results, int) else 0
        
        return {
            "execution_status": "success",
            "results": [],
            "row_count": affected_rows,
            "formatted_response": f"Successfully executed. {affected_rows} row(s) affected."
        }


    
    def _create_response_message(self, results: List[Dict], sql: str) -> str:
        row_count = len(results)
        sql_upper=sql.upper()
        if 'FROM' in sql_upper:
            parts=sql_upper.split('FROM')
            if(len(parts)>1):
                table_part=parts[1].strip().split()[0]
                table_name=table_part.replace(',','').replace(';','')
            else:
                table_name="table"

        else:
            table_name="table"            
        if row_count==0:
            return f"No results found"
        elif row_count==1:
            return f"Found 1 record from {table_name}"
        else:
            return f"Found {row_count} records from {table_name}"

    def close(self):
        """Close database connection"""
        self.db_manager.close()
        

# Node function for LangGraph
def query_executor_node(state: Dict) -> Dict:
    try:
        generated_sql=state.get("generated_sql","")
        is_safe=state.get("is_safe",False)
        executor=QueryExecutor(DATABASE_URL)
        result=executor.execute_query(generated_sql,is_safe)
        executor.close()
        return {
            "execution_status": result["execution_status"],
            "query_results": result["results"],
            "result_count": result["row_count"],
            "final_response": result["formatted_response"]
        }
    except Exception as e:
        return {
            "execution_status": "error",
            "query_results": [],
            "result_count": 0,
            "final_response": f"Execution failed: {str(e)}",
            "error": str(e)
        }
    

# Test the executor
if __name__ == "__main__":
    
    executor = QueryExecutor(DATABASE_URL)
    
    # Test Case 1: SELECT query
    print("Test 1: SELECT query")
    result = executor.execute_query(
        "SELECT * FROM customers WHERE city = 'Delhi'",
        is_safe=True
    )
    print(result)
    print()
    
    # Test Case 2: COUNT query
    print("Test 2: COUNT query")
    result = executor.execute_query(
        "SELECT COUNT(*) FROM customers",
        is_safe=True
    )
    print(result)
    print()
    
    # Test Case 3: JOIN query
    print("Test 3: JOIN query")
    result = executor.execute_query(
        "SELECT c.name, COUNT(o.id) as order_count FROM customers c LEFT JOIN orders o ON c.id = o.customer_id GROUP BY c.id",
        is_safe=True
    )
    print(result)
    print()
    
    executor.close()