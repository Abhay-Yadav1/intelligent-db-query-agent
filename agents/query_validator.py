import re
from typing import Dict, List
import sys
import os
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

class QueryValidator:
    def __init__(self):
        self.dangerous_keywords = [
            'DELETE', 'DROP', 'TRUNCATE', 'ALTER', 
            'CREATE', 'INSERT', 'UPDATE'
        ]
        # critical keywords (immediate rejection)
        self.critical_keywords = [
            'DROP DATABASE', 'DROP TABLE', 'TRUNCATE TABLE'
        ]
    def validate_query(self,sql:str)-> Dict:
        result={
            "is_safe":True,
            "risk_level":"LOW",
            "issues":[],
            "needs_approval":False,
            "sql":sql
            }
        critical_ops=self.check_critical_operations(sql)
        if(critical_ops):
            result["issues"].extend(critical_ops)
            result["is_safe"]=False
        dangerous_ops=self.check_dangerous_operations(sql)
        if (dangerous_ops):
            result['issues'].extend(dangerous_ops)
        if not self._validate_syntax(sql):
           result["issues"].append("Invalid SQL syntax")
           result["is_safe"] = False        
        result["risk_level"]=self._calc_risk_level(result["issues"])
        if result["risk_level"] in ["MEDIUM", "HIGH"]:
           result["needs_approval"] = True
    
        return result
    
    def check_critical_operations(self,sql:str)->List[str]:
        sql_upper=sql.upper()
        found=[]
        for key in self.critical_keywords:
            if key in sql_upper:
                found.append(f"CRITICAL: {key} detected")
        return found
    
    def check_dangerous_operations(self,sql:str)->List[str]:
        sql_upper=sql.upper()
        found=[]
        for keyword in self.dangerous_keywords:
            if re.search(r'\b' + keyword + r'\b', sql_upper):
                found.append(f"Dangerous operation: {keyword}")
        return found
    def _validate_syntax(self, sql: str) -> bool:
        if not sql or not sql.strip():
            return False
        if sql.count('(') != sql.count(')'):
            return False
        sql_upper = sql.strip().upper()
        valid_starts = ['SELECT', 'INSERT', 'UPDATE', 'DELETE', 'CREATE', 'DROP', 'ALTER']
        if not (sql_upper.startswith(key) for key in valid_starts):
            return False
        return True
    def _calc_risk_level(self,issues:List[str])->str:
        for issue in issues:
            if issue.startswith('CRITICAL'):
                return "HIGH"
            
            dangerous_cnt=len([i for i in issues if "Dangerous operation" in i])
            if dangerous_cnt>0:
                return "MEDIUM"
            
        return "LOW"

def query_validator_node(state:Dict)-> Dict:
    generated_sql=state.get("generated_sql","")
    validator=QueryValidator()
    validation_result=validator.validate_query(generated_sql)
    return {
        "is_safe": validation_result["is_safe"],
        "risk_level": validation_result["risk_level"],
        "validation_issues": validation_result["issues"],
        "needs_approval": validation_result["needs_approval"]
    }

if __name__ == "__main__":
    validator = QueryValidator()
    
    # Test Case 1: Safe SELECT query
    print("Test 1: Safe SELECT")
    result = validator.validate_query("SELECT * FROM customers WHERE city = 'Delhi'")
    print(result)
    print()
    
    # Test Case 2: Dangerous DELETE query
    print("Test 2: DELETE query")
    result2 = validator.validate_query("DELETE FROM customers WHERE id = 1")
    print(result2)
    print()

    print("Test 3: DROP TABLE query")
    result3 = validator.validate_query("DROP TABLE customers")
    print(result3)
    print()
    
    # Test Case 4: UPDATE query
    print("Test 4: UPDATE query")
    result4 = validator.validate_query("UPDATE customers SET city = 'Mumbai' WHERE id = 1")
    print(result4)

        
