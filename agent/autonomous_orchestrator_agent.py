import openai
import os
import json
import re
import threading
import time
from .autonomous_agent import AutonomousAgent

class AutonomousOrchestratorAgent(AutonomousAgent):
    def __init__(self, model_id, name, prompt, memory_folder):
        super().__init__(model_id, name, prompt, memory_folder)
        self.best_pool = None
        self.task = None
        self.sub_pools = []

    def extract_pool(self, text):
        agent_pattern = r'pool:\s*(\S+)'
        agent_pattern = re.compile(agent_pattern, re.IGNORECASE)
        match = re.search(agent_pattern, text)
        if match:
            agent = match.group(1)
            return agent
        else:
            return "can't not find agent"

    def extract_task(self, text):
        task_pattern = r'task:\s*(.*)'
        task_pattern = re.compile(task_pattern, re.IGNORECASE)
        match = re.search(task_pattern, text)
        if match:
            task = match.group(1)
            return task
        else:
            return "can't not find task"
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

    def set_sub_pool(self, pools):
        self.sub_pools = pools

    def run(self):
        while True:
            task = self.pool.get_task()
            if not task:
                time.sleep(1)
            if task:
                print(f"Agent {self.name} is going to process the task: {task}")
                self.process_task(task)
                self.best_pool = self.extract_pool(self.response)
                self.task = task 
                for pool in self.sub_pools:
                    if (pool.__class__.__name__ == self.best_pool):
                        pool_name = pool.__class__.__name__
                        print(f"Adding task {self.task} to {pool_name}")
                        pool.add_task(self.task)
                for pool in self.sub_pools:
                    print(f"{pool.__class__.__name__} : ")
                    print(pool.tasks)
