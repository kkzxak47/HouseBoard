from src.prompt import Prompt
import os
import openai
from openai import OpenAI
client = OpenAI()

openai.api_key = os.getenv("OPENAI_API_KEY")


class LLM:
    def __init__(self):
        self.prompt = Prompt()
        self.model = os.getenv("OPENAI_MODEL", default="gpt-4o-mini")
        self.temperature = float(os.getenv("OPENAI_TEMPERATURE", default=0.7))
        self.max_tokens = int(os.getenv("OPENAI_MAX_TOKENS", default=400))
    
    def get_response(self):
        response = client.chat.completions.create(
            model=self.model,
            messages=self.prompt.generate_prompt(),
        )
        return response.choices[0].message.content


    def add_msg(self, text, role):
        if role == "ai":
            self.prompt.add_ai_msg(text)
        else:
            self.prompt.add_user_msg(text)

    def update_memory(self, text):
        self.prompt.update_memory(text)

    def show_memory(self):
        return self.prompt.show_memory()