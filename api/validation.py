from pydantic import BaseModel

class AlertRequest(BaseModel):
    message: bool
    id: int