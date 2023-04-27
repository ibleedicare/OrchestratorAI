import argparse
import json

# create an argument parser
parser = argparse.ArgumentParser(description="Create a JSON file with specified data")
parser.add_argument("agent_name", help="name of the agent")
parser.add_argument("system_prompt_file", help="path to file containing system prompt content")
parser.add_argument("user_prompt_file", help="path to file containing assistant prompt content")

args = parser.parse_args()

# define the data to be written to the JSON file
with open(args.system_prompt_file, "r") as s, open(args.user_prompt_file, "r") as a:
    system_prompt_content = s.read()
    user_prompt_content = a.read()
data = [
    {"role": "system", "content": system_prompt_content},
    {"role": "user", "content": user_prompt_content},
    {"role": "assistant", "content": "Response: I understand, I'll just keep the code in my memory"}
]

# parse the command line arguments
args = parser.parse_args()

# write the data to the specified file
with open(f"memory/{args.agent_name}_memory.json", "w") as f:
    json.dump(data, f)

