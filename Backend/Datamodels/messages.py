from typing import List, Dict
from pydantic import BaseModel

class Message(BaseModel):
    role: str
    parts: List[str]
    
    def get_gemini_format(self) -> Dict:
        return {"role": self.role, "parts": self.parts}