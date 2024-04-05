import yaml
import os
import logging
import time
import asyncio

import google.generativeai as genai
from fastapi import FastAPI, WebSocket, HTTPException, WebSocketDisconnect
from typing import Annotated
from fastapi.responses import StreamingResponse, RedirectResponse

from Datamodels.summarize_request import SummarizeRequest
from RequestHandlers import DocumentChatHandler

app = FastAPI()

def get_gemini_api_key() -> str:
    return os.getenv("GEMINI_API_KEY", "")

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.post("/v1/model/gemini-pro:create-chat-heading")
async def create_heading(req_body):
    pass

@app.post("/v1/model/gemini-pro:summarize")
async def summarize_text(req_body: SummarizeRequest):
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
    
    def stream_model_output():
        try:
            response = model.generate_content(
                summarize_prompt,
                stream=True
            )
            
            for chunk in response:
                for char in chunk.text:
                    yield char
        except Exception:
            raise HTTPException(500, detail="Gemini model failed to respond.")
        
    return StreamingResponse(stream_model_output(), media_type="text")

@app.websocket("ws/v1/model/gemini-pro:document-chat")
async def webpage_chat(websocket: WebSocket):
    await websocket.accept()
    api_key = get_gemini_api_key()
    file_data = await websocket.receive_bytes()
    client_handler = DocumentChatHandler()
    
    try:
        while True:
            user_questions = await asyncio.wait_for(
                websocket.receive_json(), 
                timeout=10
            )
    except asyncio.TimeoutError:
        await websocket.close()
    except WebSocketDisconnect
    
    