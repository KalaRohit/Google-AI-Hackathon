from typing import List, Dict

from httpx import request
from Datamodels.Message import Message
from pydantic import BaseModel

class DocumentChatRequest(BaseModel):
    chat_id: str
    document_id: str
    history: List[Message]
    new_question: str
    
    
    def get_formatted_history(self) -> List[dict]:
        gemini_compaitible_messages = []
        for m in self.history:
            gemini_compaitible_messages.append(
                m.get_gemini_format()
            )
    
        return gemini_compaitible_messages
    
class SimplifyRequest(BaseModel):
    request_id: str
    text: str
    target_reading_level: int

class WebpageChatRequest(BaseModel):
    request_id: str
    messages: List[Message]
    newQuestion: str
    webpageContent: str
    
    def get_formatted_history(self) -> List[dict]:
        gemini_compaitible_messages = []
        for m in self.messages:
            gemini_compaitible_messages.append(
                m.get_gemini_format()
            )
    
        return gemini_compaitible_messages