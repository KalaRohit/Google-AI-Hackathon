# python >= 3.9
import os
import google.generativeai as genai

def main():
    quit_symbol = ':q'
    API_KEY = os.getenv("GEMINI_API_KEY", "")
    model = genai.GenerativeModel('gemini-pro')
    genai.configure(api_key=API_KEY)

    while True:
        user_input = input("Enter text: ")

        if user_input == quit_symbol:
            return
        
        print(f"User input is: {user_input}")
        
        response = model.generate_content(
            user_input,
            stream=True
        )

        for chunk in response:
            print(chunk.text)

if __name__ == "__main__":
    main()
