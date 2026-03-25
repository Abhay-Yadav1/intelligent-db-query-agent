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
        result={}
        wordlist = re.findall(r'\b\w+\b', sql)
        word=wordlist[0]
        