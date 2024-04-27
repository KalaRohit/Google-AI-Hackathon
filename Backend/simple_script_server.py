import yaml
import os
import asyncio

import google.generativeai as genai
from vertexai import generative_models
from fastapi import FastAPI, HTTPException, UploadFile, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware

from RequestHandlers.DocumentHandler import DocumentHandler
from RequestHandlers.DocumentChatHandler import DocumentChatHandler

from Datamodels.Requests import SummarizeRequest, DocumentChatRequest
from Datamodels.Responses import DocumentUploadResponse

app = FastAPI(root_path="/server")
origins = [
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"]
)

def get_gemini_api_key() -> str:
    return os.getenv("GEMINI_API_KEY", "")

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.post("/v1/model/gemini-pro:generate-chat-heading")
async def create_heading(req_body):
    pass


async def get_summary(req_body: SummarizeRequest):
    api_key = get_gemini_api_key()
    
    try:
        with open("./prompts/gemini-pro.yml") as prompt_file:
            summarize_prompt: str = yaml.safe_load(
                prompt_file
            )["webpage-summarize-prompt"]
    except FileNotFoundError:
        raise HTTPException(500, detail="Server failed to read prompt file.")
    
    summarize_prompt = summarize_prompt.format(
        target_reading_level=req_body.target_reading_level,
        raw_text = req_body.text
    )
        
    genai.configure(api_key=api_key, transport="grpc")    
    model = genai.GenerativeModel('gemini-pro')
    
    await asyncio.sleep(0.3)
    response = model.generate_content(summarize_prompt)
    
    try:
        return response.text
    except ValueError as e:
        print(response)
        print(response.candidates[0].safety_ratings)
        return req_body.text
    
@app.post("/v1/model/gemini-pro:simplify")
async def simplify(req_body: SummarizeRequest):
    tasks = []
    tasks.append(get_summary(req_body))
    
    return await asyncio.gather(*tasks) 

@app.options("/v1/model/gemini-pro:simplify")
async def cors():
    CORS_HEADERS = {
    "Access-Control-Allow-Origin": "*",
    "Access-Control-Allow-Methods": "*",
    "Access-Control-Allow-Headers": "*",
    "Access-Control-Max-Age": "3600",
    }
    return CORS_HEADERS

@app.post("/v1/model/gemini-pro:document-chat")
async def webpage_chat(request: DocumentChatRequest):
    print(type(request))
    chat_handler = DocumentChatHandler(request=request)
    
    return {"response": {chat_handler.model_chat()}}
    
    
    
@app.post("/v1/documents", status_code=202)
async def receive_client_file(req_body: UploadFile, background_tasks: BackgroundTasks):
    if req_body.content_type != "application/pdf":
        raise HTTPException(status_code=415, detail="User did not submit a PDF.")
    
    doc_handler = DocumentHandler(document=req_body)
    document_id = str(doc_handler.document_id)
    background_tasks.add_task(doc_handler.one_shot_embed)
    
    return DocumentUploadResponse(document_id=document_id, error=False).model_dump_json(indent=4)

@app.delete("v1/documents/{doc_id}", status_code=202)
async def mark_document_for_deletion():
    pass