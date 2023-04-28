import yaml
from agent import *
from colorama import Fore, Style
import threading

with open("config.yaml", "r") as f:
    config = yaml.safe_load(f)

agents = []
for agent_config in config["agents"]:
    agent_type = globals()[agent_config["agent_type"]]
    agent = agent_type(
        model_id=agent_config["model_id"],
        name=agent_config["name"].strip(),
        prompt=agent_config["prompt"],
        memory_folder=agent_config["chat_folder"]
    )
    agents.append(agent)

for agent in agents:
    if (agent.name == "OrchestratorAgent"):
        orchestrator = agent

agents.pop(agents.index(orchestrator))
current_token = 0
shared_memory = []
next_task = None
while True:
    best_agent = None
    agent = orchestrator
    if (agent.name == "OrchestratorAgent"):
        if (next_task == None):
            user_message = "Goal: " + input(f"{Fore.GREEN}User:{Style.RESET_ALL} ")
            next_task = user_message
        if (user_message == "quit"):
            break
        if (user_message == "!history"):
            print(f"Current history: {orchestrator.chat_history}")
        if (user_message == "!user_prompt"):
            with open("user_prompt.txt", "r") as f:
                user_message = f.read()
        thinking_thread = threading.Thread(target=agent.thinking_animation)
        send_message_thread = threading.Thread(target=agent.send_message, args=(next_task,))
        send_message_thread.start()
        thinking_thread.start()
        send_message_thread.join()
        thinking_thread.join()
        response = agent.response
        best_agent = agent.extract_agent(response)
        task = agent.extract_task(response)
        current_token += agent.token
        print(f"Token usage : {current_token}")
        print(f"Price : {current_token/1000 * 0.002}")
    for agent in agents:
        if (agent.name == best_agent):
            print(f"{Fore.BLUE}The task will be : {Style.RESET_ALL}{task}")
            do_task = input(f"Give the task to {best_agent} ?")
            if (do_task == "n"):
                break
            if (len(shared_memory) > 0):
                agent.chat_history.append(shared_memory[-1])
            thinking_thread = threading.Thread(target=agent.thinking_animation)
            send_message_thread = threading.Thread(target=agent.send_message, args=(task,))
            send_message_thread.start()
            thinking_thread.start()
            send_message_thread.join()
            thinking_thread.join()
            response = agent.response
            code = agent.extract_code(response)
            filename = agent.extract_filename(response)
            next_task = f"Goal: {agent.extract_goal(response)}. Don't give this task to {best_agent}"
            agent.write_to_file("generated", filename, code)
            current_token += agent.token
            print(f"Token usage : {current_token}")
            print(f"Price : {current_token/1000 * 0.002}")
            shared_memory.append({"role": "assistant", "content": response})
#while True:
#    user_message = input(f"{Fore.GREEN}User:{Style.RESET_ALL} ")
#    if (user_message == "quit"):
#        break
#    if (user_message == "!user_prompt"):
#        with open("user_prompt.txt", "r") as f:
#            user_message = f.read()
#    thinking_thread = threading.Thread(target=agent.thinking_animation)
#    send_message_thread = threading.Thread(target=agent.send_message, args=(user_message,))
#    send_message_thread.start()
#    thinking_thread.start()
#    send_message_thread.join()
#    thinking_thread.join()
#    response = agent.response
#    code = agent.extract_code(response)
#    filename = agent.extract_filename(response)
#    agent.write_to_file("generated", filename, code)
