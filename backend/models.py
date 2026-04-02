from pydantic import BaseModel
from typing import List, Optional

class QueryRequest(BaseModel):
    question:str
    

class QueryResponse(BaseModel):
    question:str
    sql:str
    status:str
    results:List
    message:str
    error:str | None = None
  