import openai
import os
import json
import time
from colorama import Fore, Style
import threading

class AutonomousAgent(threading.Thread):
    def __init__(self, model_id, name, prompt, memory_folder):
        super().__init__()
        self.pool = None
        openai.api_key = os.getenv("OPENAI_API_KEY")
        self.response = None
        self.stop_thinking = False
        self.model_id = model_id
        self.name = name
        with open(f"prompt/{prompt}", "r") as f:
            self.prompt = f.read()
        self.token = 0
        self.chat_history = []
        self.chat_file = f"{memory_folder}/{self.name}_memory.json"
        if os.path.isfile(self.chat_file) and os.path.getsize(self.chat_file) > 0:
            while True:
                choice = input(f"Do you want to load the chat history from file for {self.name} ? (Y/N)").lower()
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
        self.stop_thinking = False
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
        self.stop_thinking = True
        self.show_pretty_message(message)
        self.response = message
        return message

    def get_current_chat_history(self):
        print(self.chat_history)

    def save_chat_history(self):
        with open(self.chat_file, "w") as f:
            json.dump(self.chat_history, f)

    def thinking_animation(self):
        animation = "|/-\\"
        i = 0
        while self.stop_thinking != True:
            print("Agent {} is thinking... {}".format(self.name, animation[i]), end="\r")
            i = (i + 1) % len(animation)
            time.sleep(0.1)

    def show_pretty_message(self, response):
        print(f"{Fore.CYAN}{self.name}:{Style.RESET_ALL}\n{response}")

    def set_pool(self, pool):
        self.pool = pool

    def set_orchestrator_pool(self, pool):
        self.orchestratorPool = pool

    def process_task(self, task):
        # init thread
        thinking_thread = threading.Thread(target=self.thinking_animation, args=())
        send_message_thread = threading.Thread(target=self.send_message, args=(task, ))

        # start thread
        send_message_thread.start()
        thinking_thread.start()

        # join thread
        send_message_thread.join()
        thinking_thread.join()


    def run(self):
        while True:
            task = self.pool.get_task()
            if not task:
                break
            if task:
                print(f"Agent {self.name} is going to process the task: {task}")
                self.send_message(task)
