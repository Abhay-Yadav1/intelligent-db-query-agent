import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from main import DatabaseQueryAgent

class AgentService:
    def __init__(self):
        self.agent = DatabaseQueryAgent()
        
    
    def process_query(self, question: str) -> dict:
        """Process a query and return results"""
        result=self.agent.query(question)
        return result
       

# Create singleton instance
agent_service = AgentService()