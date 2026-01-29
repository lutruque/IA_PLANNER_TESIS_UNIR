from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional

class PlanRequest(BaseModel):
    region: str
    days: int = Field(ge=1, le=10)
    profile: List[str]
    city_base: str
    constraints: Optional[Dict[str, Any]] = None

class PlanAndEmailRequest(PlanRequest):
    to_email: str
    subject: str
