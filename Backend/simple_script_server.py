import yaml
import os
import logging

import google.generativeai as genai
from fastapi import FastAPI

from Datamodels.summarize_request import geminiProSummarizeRequestBody

app = FastAPI()

def get_gemini_api_key() -> str:
    return os.getenv("GEMINI_API_KEY", "")

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.post("/chatbot/gemini-pro:summarize")
async def summarize_text(req_body: geminiProSummarizeRequestBody):
    api_key = get_gemini_api_key()
    with open("./prompts/gemini-pro.yml") as prompt_file:
        summarize_prompt: str = yaml.safe_load(
            prompt_file
        )["webpage-summarize-prompt"]
    
    summarize_prompt = summarize_prompt.format(
        target_reading_level=req_body.target_reading_level,
        summarizable_text=req_body.text
    )
    
    genai.configure(api_key=api_key, transport="grpc")
    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content(
        summarize_prompt,
        stream=True
    )
    
    full_response = ""
    
    for chunk in response:
        full_response += chunk.text
            
    return {"response": full_response}