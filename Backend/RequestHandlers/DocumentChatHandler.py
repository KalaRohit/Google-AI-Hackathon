import os
import re
import pprint

import google.generativeai as genai 
from qdrant_client import QdrantClient
from vertexai.language_models import TextEmbeddingModel

import yaml

from Datamodels.Requests import DocumentChatRequest

class DocumentChatHandler:
    def __init__(self, request: DocumentChatRequest) -> None:
        self.request = request
        
    def get_relevant_context_from_vector_store(self, document_id: str, search_query: str, limit: int = 5) -> str:
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
            limit=20
        )
        
        context = ""
    
        for info in search_result:
            payload: str = str(info.payload)
            
            context += payload
        
        return context
            
    def model_chat(self):
        messages = self.request.get_formatted_history()
        pprint.pprint(messages)
        API_KEY = os.getenv("GEMINI_API_KEY", "")
        model = genai.GenerativeModel(
            'gemini-pro', 
            tools=[self.get_relevant_context_from_vector_store]
        )
        genai.configure(api_key=API_KEY, transport='rest')
        
        with open("./prompts/gemini-pro.yml", 'r') as readfile:
            prompt: str = yaml.safe_load(readfile)["document-chatter-prompt"]
            prompt = prompt.format(
                document_id=self.request.document_id,
                user_query=self.request.new_question
            )
        
        chat = model.start_chat(
            history=messages,
            enable_automatic_function_calling=True
        )
        
        response = chat.send_message(
            prompt
        )
        
        return response.text
        
        