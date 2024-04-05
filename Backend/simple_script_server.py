import yaml
import os
import logging

import google.generativeai as genai
from fastapi import FastAPI
from fastapi.responses import StreamingResponse

from Datamodels.summarize_request import SummarizeRequest

app = FastAPI()

def get_gemini_api_key() -> str:
    return os.getenv("GEMINI_API_KEY", "")

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.post("/v1/model/gemini-pro:summarize")
async def summarize_text(req_body: SummarizeRequest):
    api_key = get_gemini_api_key()
    with open("./prompts/gemini-pro.yml") as prompt_file:
        summarize_prompt: str = yaml.safe_load(
            prompt_file
        )["webpage-summarize-prompt"]
    
    summarize_prompt = summarize_prompt.format(
        target_reading_level=req_body.target_reading_level,
        raw_text = req_body.text
    )
    
    genai.configure(api_key=api_key, transport="grpc")    
    model = genai.GenerativeModel('gemini-pro')
    
    def stream_model_output():
        response = model.generate_content(
            summarize_prompt,
            stream=True
        )
        
        for chunk in response:
            for char in chunk.text:
                yield char
    
    return StreamingResponse(stream_model_output(), media_type="text")

@app.post("/v1/model/gemini-pro:chat")
async def webpage_chat(req_body):
    api_key = get_gemini_api_key()