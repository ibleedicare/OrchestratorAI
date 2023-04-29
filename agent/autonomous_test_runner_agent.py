import openai
import os
import json
import re
import time
import threading
from .autonomous_dev_agent import AutonomousDevAgent
import subprocess


class AutonomousTestRunnerAgent(AutonomousDevAgent):
    def __init__(self, model_id, name, prompt, memory_folder):
        super().__init__(model_id, name, prompt, memory_folder)

    def process_task(self, task):
        # init thread
        thinking_thread = threading.Thread(target=self.thinking_animation, args=())
        filename = self.extract_filename(task)
        response = self.run_test(filename)
        send_message_thread = threading.Thread(target=self.send_message, args=(response, ))

        # start thread
        send_message_thread.start()
        thinking_thread.start()

        # join thread
        send_message_thread.join()
        thinking_thread.join()
    def run_test(self, filename):
        # Define the command to run pytest
        pytest_cmd = f'pytest -qx generated/{filename}'

        # Run pytest using subprocess
        process = subprocess.Popen(pytest_cmd.split(), stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        # Get the output and error messages
        stdout, stderr = process.communicate()

        # Get the return code of pytest
        return_code = process.returncode

        # Check if pytest passed or failed
        if return_code == 0:
            print('All tests passed!')
            return stdout.decode('utf-8')
        else:
            print("Failing test")
            return stdout.decode('utf-8')
