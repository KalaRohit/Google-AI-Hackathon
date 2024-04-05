import google.generativeai as genai 
from Datamodels.docchat_request import DocumentChatRequest
from Datamodels.Message import Message

class DocumentChatHandler:
    def __init__(self, document: bytes, api_key: str) -> None:
        self.api_key = api_key
        self.document = document
        
    
    def parse_document(self):
        pass
    
    def one_shot_embed(self):
        pass
    
    def generate_context_for_question(self):
        pass
    
    def chat(self, request: DocumentChatRequest):
        gemini_compaitible_history = []
         
        for message in request.history:
            gemini_compaitible_history.append(message.get_gemini_format())
        
        message = \
            Message(role="user", parts=[request.new_question]).get_gemini_format()
        gemini_compaitible_history.append(message)
        genai.configure(api_key=self.api_key, transport="grpc")    
        model = genai.GenerativeModel('gemini-pro')
        response = model.generate_content(
            gemini_compaitible_history
        )
        
        return response.text
    
    