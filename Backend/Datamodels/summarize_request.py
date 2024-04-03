from pydantic import BaseModel

class geminiProSummarizeRequestBody(BaseModel):
    request_id: str
    text: str
    target_reading_level: int