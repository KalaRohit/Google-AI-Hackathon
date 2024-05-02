import os
import yaml
import pprint

import google.generativeai as genai
from Datamodels.Requests import WebpageChatRequest 


class WebpageChatHandler:
    def __init__(self, request: WebpageChatRequest) -> None:
        self.request = request
        
    def model_chat(self):
        messages = self.request.get_formatted_history()
        pprint.pprint(messages)
        API_KEY = os.getenv("GEMINI_API_KEY", "")
        model = genai.GenerativeModel(
            'gemini-pro'
        )
        
        genai.configure(api_key=API_KEY, transport='grpc')
        
        with open("./prompts/gemini-pro.yml", 'r') as readfile:
            prompt: str = yaml.safe_load(readfile)["webpage-chatter-prompt"]
            prompt = prompt.format(
                webpage_content=self.request.webpageContent,
                user_question=self.request.newQuestion
            )
        
        pprint.pprint(self.request.get_formatted_history())
        
        chat = model.start_chat(
            history=self.request.get_formatted_history(),
        )
        
        
        
        response = chat.send_message(
            prompt
        )
        
        try:
            return response.text
        except Exception as e: 
            return f"Sorry, I ran into an error \n{e}"
        