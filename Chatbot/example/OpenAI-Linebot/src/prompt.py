import os

MSG_LIMIT = int(os.getenv("MSG_LIMIT", default=10))

memory = os.getenv("MEMORY",default="你的名字是小小汪，說話會以「小狗狗我覺得」開頭")

class Prompt:
    def __init__(self):
        self.message = [{"role": "system", "content": memory}]

    def add_ai_msg(self, text):
        if len(self.message) >= MSG_LIMIT:
            self.remove_msg()
        self.message.append({"role": "assistant", "content": text})

    def add_user_msg(self, text):
        if len(self.message) >= MSG_LIMIT:
            self.remove_msg()
        self.message.append({"role": "user", "content": text})

    def remove_msg(self):
        self.message.pop(1)

    def generate_prompt(self):
        return self.message
    
    def update_memory(self, text):
        self.message[0] = {"role": "system", "content": text}
        
    def show_memory(self):
        return self.message[0]["content"]

