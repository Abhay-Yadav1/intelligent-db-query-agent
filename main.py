"""
Intelligent Database Query Agent
Main entry point for the application
"""

import sys
import os
from typing import Dict, Any

# Add project root to path
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

from graphs.complete_workflow import create_complete_workflow
from dotenv import load_dotenv

load_dotenv()

class DatabaseQueryAgent:
    """Main agent interface"""
    
    def __init__(self):
        """Initialize the agent"""
        self.workflow = create_complete_workflow()
        print("✅ Intelligent Database Query Agent initialized")
    
    def query(self, question: str, thread_id: str = "default") -> Dict[str, Any]:
        initial_state=self._create_initial_state(question)
        config={"configurable":{"thread_id":thread_id}}
        result=self.workflow.invoke(initial_state,config)
        print("\n=== DEBUG: Complete Result ===")
        for key, value in result.items():
             print(f"{key}: {value}")
             print("=" * 60)
        if result.get("needs_approval") and result.get("human_approved") is None:
            print("\n" + "=" * 60)
            print(result.get("approval_message", "Approval required"))
            print("=" * 60)
            approval=input("\n✋ Approve? (yes/no): ").strip().lower()
            if approval in ['yes','y']:
                self.workflow.update_state(config,{"human_approved": True, "is_safe": True})
                result=self.workflow.invoke(None, config)   
            else:
                result["execution_status"] = "rejected"
                result["final_response"] = "Query execution rejected by user"    
        return self._format_final_response(result)        
       
    
    def _create_initial_state(self, question: str) -> Dict:
        return {
        "question": question,
        "all_tables": ["customers", "orders"], 
        "selected_tables": [],
        "generated_sql": "",
        "is_safe": True,
        "risk_level": "LOW",
        "validation_issues": [],
        "needs_approval": False,
        "execution_status": "",
        "query_results": [],
        "result_count": 0,
        "final_response": "",
        "human_approved": None,
        "approval_message": "",
        "error": ""
    }
    
    def _format_final_response(self, result: Dict) -> Dict:
        return {
        "question": result.get("question", ""),
        "sql": result.get("generated_sql", ""),
        "status": result.get("execution_status", "unknown"),
        "results": result.get("query_results", []),
        "message": result.get("final_response", ""),
        "error": result.get("error", "")
    }

# Interactive CLI
def main():
    """Main CLI interface"""
    print("=" * 60)
    print("🤖 Intelligent Database Query Agent")
    print("=" * 60)
    print()
    
    # Initialize agent
    agent = DatabaseQueryAgent()
    print()
    
    # Interactive loop
    while True:
        print("-" * 60)
        question = input("❓ Enter your question (or 'quit' to exit): ")
        
        if question.lower() in ['quit', 'exit', 'q']:
            print("\n👋 Goodbye!")
            break
        
        if not question.strip():
            print("⚠️  Please enter a valid question")
            continue
        
        print()
        print("🔄 Processing your query...")
        print()
        
        try:
            # Process query
            result = agent.query(question)
            
            # Display results
            print("=" * 60)
            print("📊 RESULTS")
            print("=" * 60)
            print(f"Question: {result['question']}")
            print(f"Generated SQL: {result['sql']}")
            print(f"Status: {result['status']}")
            
            if result['status'] == 'success':
                print(f"Results: {result['results']}")
                print(f"Message: {result['message']}")
            else:
                print(f"Error: {result.get('error', 'Unknown error')}")
            
            print()
            
        except Exception as e:
            print(f"❌ Error: {str(e)}")
            print()

if __name__ == "__main__":
    main()