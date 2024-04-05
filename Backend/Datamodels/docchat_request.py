from typing import List
from Datamodels.Message import Message
from pydantic import BaseModel

class DocumentChatRequest(BaseModel):
    chatID: str
    history: List[Message]
    new_question: str
    