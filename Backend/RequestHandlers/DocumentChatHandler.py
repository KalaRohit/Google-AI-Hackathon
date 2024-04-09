import os

import google.generativeai as genai 
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct
from vertexai.language_models import TextEmbeddingModel
import yaml

from Datamodels.Requests import DocumentChatRequest
# from Datamodels.Responses import DocumentUploadResponse
from Datamodels.Message import Message
import pprint

class DocumentChatHandler:
    def __init__(self, request: DocumentChatRequest) -> None:
        self.request = request
        
    
    def get_relevant_context_from_vector_store(self, document_id: str, search_query: str) -> str:
        """
        Query a vector store to get some relevant context on a search query
        
        Args: 
        
            document_id: str
                The name/id of the document
            search_query: str
                The search query is the string which will first be embedded using
                the textembedding-gecko@001, which is then used to perform
                ANN search using QDrantDB.
        
        Returns:
            str
                The context fetched from vector store.
        """
        qdrant_client = QdrantClient(url="http://localhost:6333")
        print(search_query)
        embedding_model = TextEmbeddingModel.from_pretrained("textembedding-gecko@001")
        embedded_question = embedding_model.get_embeddings([search_query])[0].values
        search_result = qdrant_client.search(
            collection_name=document_id,
            query_vector=embedded_question,
            limit=3
        )
        
        context = ""
    
        for info in search_result:
            payload: str = str(info.payload)
            
            context += payload
        
        print(context.replace("\\n", ""))
        
        return context.replace("\\n", "")
    
    def summarize_text(self, text: str) -> str:
        """
        
        """
        print("In summarize text...")
        API_KEY = os.getenv("GEMINI_API_KEY", "")
        model = genai.GenerativeModel(
            'gemini-pro'
        )
        genai.configure(api_key=API_KEY)
        
        summary = model.generate_content(text)
        
        return summary
    
    def model_chat(self):
        messages = self.request.get_formatted_history()
        pprint.pprint(messages)
        API_KEY = os.getenv("GEMINI_API_KEY", "")
        model = genai.GenerativeModel(
            'gemini-pro', 
            tools=[self.get_relevant_context_from_vector_store, self.summarize_text]
        )
        genai.configure(api_key=API_KEY, transport='rest')
        
        with open("./prompts/gemini-pro.yml", 'r') as readfile:
            prompt: str = yaml.safe_load(readfile)["document-chatter-prompt"]
            prompt = prompt.format(
                document_id=self.request.document_id,
                user_query=self.request.new_question
            )
        
        print(prompt)
        chat = model.start_chat(history=messages, 
            enable_automatic_function_calling=True
        )
        
        response = chat.send_message(
            prompt
        )
        
        return response.text
        
        