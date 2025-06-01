from pydantic import BaseModel

class AlertRequest(BaseModel):
    id: int