import openai
import os
import json
import re
from .autonomous_agent import AutonomousAgent

class AutonomousDevAgent(AutonomousAgent):
    def __init__(self, model_id, name, prompt, memory_folder):
        super().__init__(model_id, name, prompt, memory_folder)

    def extract_code(self, text):
        start = text.find("```")
        end = text.rfind("```")

        code = text[start+3:end].strip()

        if (code.split('\n')[0] == "python"):
            return code.split('\n', 1)[1]
        return code

    def extract_filename(self, text):
        filename_pattern = r'filename:\s*(\S+)'
        filename_pattern = re.compile(filename_pattern, re.IGNORECASE)
        match = re.search(filename_pattern, text)
        if match:
            filename = match.group(1)
            return filename
        else:
            return "ai_generated.py"

    def extract_goal(self, text):
        goal_pattern = r'Next Goal:?\s*(.*)'
        goal_pattern = re.compile(goal_pattern, re.IGNORECASE)
        match = re.search(goal_pattern, text)
        if match:
            goal = match.group(1)
            return goal
        else:
            return "ai_generated.py"

    def write_to_file(self, path, filename, content):
        with open(f"{path}/{filename}", "w") as f:
            f.write(content)
        print(f"Program written to {path}/{filename}")
