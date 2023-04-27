import openai
import os
import json
import re
from .autonomous_agent import AutonomousAgent

class AutonomousOrchestratorAgent(AutonomousAgent):
    def __init__(self, model_id, name, prompt, memory_folder):
        super().__init__(model_id, name, prompt, memory_folder)

    def extract_agent(self, text):
        agent_pattern = r'agent:\s*(\S+)'
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

