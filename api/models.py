from pydantic import BaseModel
from typing import Optional, List, Dict, Any

class AuditRequest(BaseModel):
    query: str
    top_k: Optional[int] = 5
    dataset_id: Optional[str] = None

class AuditResponse(BaseModel):
    risk_score: float
    risk_level: str  # "LOW", "MEDIUM", "HIGH"
    explanation: str
    evidence: List[Dict[str, Any]]
    sources: List[str]
    timestamp: str
