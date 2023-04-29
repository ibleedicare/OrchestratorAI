import yaml
from agent import *
from agent.shared_memory import SharedMemory
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
# All pool
devPool = DevPool([])
testerPool = TesterPool([])
testRunnerPool = TestRunnerPool([])
orchestratorPool = Pool([])

quitPool = QuitPool([])
shared_memory = SharedMemory([])
orchestrator_memory = SharedMemory([])
best_agent = None
# Set orchestrator pool
orchestrator.set_pool(orchestratorPool)
orchestrator.set_sub_pool([devPool, testerPool, testRunnerPool])
orchestrator.set_shared_memory(orchestrator_memory)
# set new task
if (next_task == None):
    user_message = input(f"{Fore.GREEN}User:{Style.RESET_ALL} ")
    if (user_message == "!user_prompt"):
        with open("user_prompt.txt", "r") as f:
            user_message = f.read()
    next_task = f"Goal: {user_message}"

# Process
orchestratorPool.add_task(user_message)
orchestrator.daemon = True
orchestrator.start()

#current_token += orchestrator.token
#print(f"Token usage : {current_token}")
#print(f"Price : {current_token/1000 * 0.002}")

for agent in agents:
    if (agent.__class__.__name__ == "AutonomousDevAgent"):
        agent.set_pool(devPool)
    if (agent.__class__.__name__ == "AutonomousTesterDevAgent"):
        agent.set_pool(testerPool)
    if (agent.__class__.__name__ == "AutonomousTestRunnerAgent"):
        agent.set_pool(testerPool)
    agent.set_orchestrator_pool(orchestratorPool)
    agent.set_shared_memory(shared_memory)
    agent.daemon = True

for agent in agents:
    agent.start()

for agent in agents:
    agent.join()

orchestrator.join()

while len(quitPool.tasks) == 0:
    time.sleep(1)
