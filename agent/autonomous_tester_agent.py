import openai
import os
import json
import re
import time
from .autonomous_dev_agent import AutonomousDevAgent

class AutonomousTesterDevAgent(AutonomousDevAgent):
    def __init__(self, model_id, name, prompt, memory_folder):
        super().__init__(model_id, name, prompt, memory_folder)
