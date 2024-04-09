import uuid
from fastapi import UploadFile
from typing import List, AsyncGenerator, Tuple
from io import BytesIO

from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct
from vertexai.language_models import TextEmbeddingModel

import PyPDF2

class DocumentHandler:
    def __init__(self, document: UploadFile) -> None:
        self.document = document
        self.document_content_bytes = document.file.read() # Need to keep this in scope using this variable
        self.vector_namespace = "VECTOR: "
        self.document_id = uuid.uuid4()
    
    async def parse(self, n_size = 1000) -> AsyncGenerator[str, List[float]]:
        pdf_reader = PyPDF2.PdfReader(BytesIO(self.document_content_bytes))
        embedding_model = TextEmbeddingModel.from_pretrained("textembedding-gecko@001")
        
        for page in pdf_reader.pages:
            text = page.extract_text()
            for i in range(0, len(text), n_size):
                chunk = text[i:i + n_size]
                chunk_string = str(chunk)
                embeddings = embedding_model.get_embeddings([chunk_string])
                yield chunk_string, embeddings[0].values

    async def one_shot_embed(self) -> str:
        '''
        Embeds document and returns the collection id for downstream use.
        '''
        
        qdrant_client = QdrantClient(url="http://localhost:6333")
        qdrant_client.create_collection(
            collection_name=str(self.document_id),
            vectors_config=VectorParams(size=768, distance=Distance.COSINE), 
        )
        
        async for page_text, embeddings in self.parse():
            vector_id = uuid.uuid4()
            vector_id = str(vector_id)
            
            qdrant_client.upsert(
                collection_name=self.document_id,
                points=[PointStruct(id=vector_id, vector=embeddings, payload={"content": page_text})]
            )
                
        return str(self.document_id)