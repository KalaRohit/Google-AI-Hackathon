from pydantic import BaseModel, Field

class DocumentUploadResponse(BaseModel):
    document_id: str
    error: bool
    description: str = Field(default="The document was uploaded.")