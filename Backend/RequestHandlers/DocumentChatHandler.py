import google.generativeai as genai 
from Datamodels.docchat_request import DocumentChatRequest
from Datamodels.Message import Message
from vertexai.language_models import TextEmbeddingModel
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct
from io import BytesIO
from typing import List
import PyPDF2

class DocumentChatHandler:
    def __init__(self, document: bytes, api_key: str, document_name: str) -> None:
        self.api_key = api_key
        self.document = document
        self.document_name = document_name
        
    async def parse_document(self, n_size = 300):
        pdf = BytesIO(self.document)
        pdf_reader = PyPDF2.PdfReader(pdf)
        
        for page in pdf_reader.pages:
            text = page.extract_text()
            for i in range(0, len(text), n_size):
                chunk = text[i:i + n_size]
                chunk_string = str(chunk)
                print(chunk_string)
                yield chunk_string
    
    
    async def embed_text(self):
        print("Embedding Text...")
        
        embedding_model = TextEmbeddingModel.from_pretrained("textembedding-gecko@001")
        async for page_text in self.parse_document():
            embeddings = embedding_model.get_embeddings([page_text])
            vector = embeddings[0].values
        
            yield vector, page_text
        
    async def one_shot_embed(self):
        print("Embedding Collection...")
        qdrant_client = QdrantClient(url="http://localhost:6333")
        qdrant_client.create_collection(
            collection_name=self.document_name,
            vectors_config=VectorParams(size=768, distance=Distance.COSINE)
        )

        
        
        index = 0
        async for vector, text in self.embed_text():
            qdrant_client.upsert(
                collection_name=self.document_name,
                points=[PointStruct(id=index, vector=vector, payload={"key": text})]
            )
            
            index += 1
               
    async def generate_context_for_question(self, question: str):
        print("Context Collection...")
        qdrant_client = QdrantClient(url="http://localhost:6333")
        embedding_model = TextEmbeddingModel.from_pretrained("textembedding-gecko@001")
        embedded_question = embedding_model.get_embeddings([question])[0].values
        search_result = qdrant_client.search(
            collection_name=self.document_name,
            query_vector=embedded_question
        )
        
        context = ""
    
        for info in search_result:
            payload: str = str(info.payload)
            
            context += payload
        
        return context
        
    
    async def chat(self, request: DocumentChatRequest):
        gemini_compaitible_history = []
         
        for message in request.history:
            gemini_compaitible_history.append(message.get_gemini_format())
        print("One shot embedding...")
        
        context = await self.generate_context_for_question(question=request.new_question)
        
        request.new_question += f"Additional information to help you answer this question: {context}"
        
        print(request.new_question)
        message = \
            Message(role="user", parts=[request.new_question]).get_gemini_format()
        gemini_compaitible_history.append(message)
        genai.configure(api_key=self.api_key, transport="grpc")    
        model = genai.GenerativeModel('gemini-pro')
        
        response = model.generate_content(
            gemini_compaitible_history
        )
        
        return response.text
    
    