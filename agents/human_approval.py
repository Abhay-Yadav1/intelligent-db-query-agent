from typing import Dict
import sys
import os

# Fix import path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

def create_approval_message(state: Dict) -> str:
    sql=state.get("generated_sql","")
    risk_level=state.get("risk_level","UNKNOWN")
    issues=state.get("validation_issues",[])
    message=f"""
           ⚠️  APPROVAL REQUIRED ⚠️
           
           The following query requires your approval before execution:
           
           SQL Query:
           {sql}
           
           Risk Level: {risk_level}
           
           Issues Detected:
          """
    if issues:
        for issue in issues:
            message+=f" • {issue}\n"
    else:
        message += "  • None\n"
    message+="\nDo you approve execution of this query? (Yes/No)"
    return message    

def human_approval_node(state: Dict) -> Dict:
    message=create_approval_message(state)
    return {
        "approval_message": message,
        "human_approved": None  
    }


def process_approval_response(approved: bool, state: Dict) -> Dict:
    if approved:
        return {
            "human_approved":True,
            "is_safe":True,
            "final_response":"Query approved by human. Executing..."
        }
    else:
        return {
            "human_approved": False,
            "is_safe": False,  # Block execution
            "execution_status": "rejected",
            "final_response": "Query execution rejected by human."
        }


# Test
if __name__ == "__main__":
    # Mock state
    test_state = {
        "question": "Delete customers from Delhi",
        "generated_sql": "DELETE FROM customers WHERE city = 'Delhi'",
        "risk_level": "MEDIUM",
        "validation_issues": ["Dangerous operation: DELETE"],
        "needs_approval": True
    }
    
    # Test approval message creation
    message = create_approval_message(test_state)
    print("Approval Message:")
    print(message)
    print()
    
    # Test approval
    print("Scenario 1: Human approves")
    result = process_approval_response(True, test_state)
    print(result)
    print()
    
    # Test rejection
    print("Scenario 2: Human rejects")
    result = process_approval_response(False, test_state)
    print(result)