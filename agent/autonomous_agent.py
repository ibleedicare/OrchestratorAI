import openai
import os
import json

class AutonomousAgent:
    def __init__(self, model_id, name, prompt, memory_folder):
        openai.api_key = os.getenv("OPENAI_API_KEY")
        self.model_id = model_id
        self.name = name
        self.prompt = prompt
        self.token = 0
        self.chat_history = []
        self.chat_file = f"{memory_folder}/{self.name}_memory.json"
        if os.path.isfile(self.chat_file) and os.path.getsize(self.chat_file) > 0:
            while True:
                choice = input("Do you want to load the chat history from file? (Y/N)").lower()
                if choice == "y":
                    with open(self.chat_file, "r") as f:
                        self.chat_history = json.load(f)
                    if len(self.chat_history) > 0:
                        last_message = self.chat_history[-1]["content"]
                        print(f"Last message in memory: {last_message}")
                    break
                elif choice == "n":
                    self.chat_history.append({"role": "system", "content": self.prompt})
                    break
                else:
                    print("Invalid choice. Please enter Y or N.")
        else:
            self.chat_history.append({"role": "system", "content": self.prompt})

    def send_message(self, user_message):
        self.chat_history.append({"role": "user", "content": user_message})
        response = openai.ChatCompletion.create(
            model=self.model_id,
            messages=self.chat_history,
        )
        message = response.choices[0].message.content.strip()
        self.chat_history = [d for d in self.chat_history if d.get('role') == 'system']
        self.chat_history.append({"role": "assistant", "content": message})
        self.save_chat_history()
        self.token += response.usage.total_tokens
        return message

    def get_current_chat_history(self):
        print(self.chat_history)

    def save_chat_history(self):
        with open(self.chat_file, "w") as f:
            json.dump(self.chat_history, f)
