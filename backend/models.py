from pydantic import BaseModel
from typing import Optional

class TaskResponse(BaseModel):
    task_id: str

class TaskStatus(BaseModel):
    status: str  # pending, processing, completed, failed
    result_url: Optional[str] = None
    error: Optional[str] = None