from agent import AutonomousAgent

prompt = """
Your name is Aether. You are a software Engineer. You have special knowledge about python3.

Your Task is to write robust code.

You will converse with the following structure, Code should only contain python3 code:

Code:
Reasoning:
Critique:
"""
agent = AutonomousAgent("gpt-3.5-turbo", "Aether", prompt, "memory")

def extract_code(text):
    start = text.find("```")
    end = text.rfind("```")

    code = text[start+3:end].strip()

    return code

while True:
    user_message = input("User: ")
    response = agent.send_message(user_message)
    print("=== DEBUG ===")
    print(agent.get_current_chat_history())
    print("=== DEBUG ===")
    print(f"Agent: {agent.token}\n{response}")
    with open("generated/ai_game.py", "w") as f:
        f.write(extract_code(response))
    continue_conversation = input("Do you want to continue ? (y/n)")
    if (continue_conversation == "n"):
        break
