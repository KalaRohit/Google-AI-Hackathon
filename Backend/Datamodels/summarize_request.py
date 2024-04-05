from pydantic import BaseModel

class SummarizeRequest(BaseModel):
    request_id: str
    text: str
    target_reading_level: int