import os
import time
import yaml

from fastapi import HTTPException
import google.generativeai as genai
from retry import retry

from Datamodels.Requests import SummarizeRequest

def get_gemini_api_key() -> str:
    return os.getenv("GEMINI_API_KEY", "")

@retry(tries=3, delay=2)
def handle_simplify_request(req_body: SummarizeRequest):
    api_key = get_gemini_api_key()
    time.sleep(0.2)
    
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
    
    response = model.generate_content(summarize_prompt)
    
    try:
        return response.text
    except ValueError as e:
        print(response)
        print(response.candidates[0].safety_ratings)
        return req_body.text