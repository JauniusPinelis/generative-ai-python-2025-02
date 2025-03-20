from rich import print
import os 
from dotenv import load_dotenv
import requests
from openai import OpenAI

import json

load_dotenv()

openai_api_key = os.getenv("OPENAI_API_KEY")
if openai_api_key is None:
    print("Please set OPENAI_API_KEY in .env file")

def get_weather(latitude: str, longitude: str):
    response = requests.get(f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&current=temperature_2m,wind_speed_10m&hourly=temperature_2m,relative_humidity_2m,wind_speed_10m")
    data = response.json()
    return data['current']['temperature_2m']

def write_to_file(content: str, filename: str = "output.txt"):
        with open(filename, 'w') as file:
            file.write(content)
        return os.path.abspath(filename)


client = OpenAI(
    base_url="https://models.inference.ai.azure.com",
    api_key=openai_api_key
)

# {"latitude":48.8566,"longitude":2.3522}

tools = [{
    "type": "function",
    "function": {
        "name": "get_weather",
        "description": "Get current temperature for provided coordinates in celsius.",
        "parameters": {
            "type": "object",
            "properties": {
                "latitude": {"type": "number"},
                "longitude": {"type": "number"}
            },
            "required": ["latitude", "longitude"],
            "additionalProperties": False
        },
        "strict": True
    }
}, {
    "type": "function",
    "function": {
        "name": "write_to_file",
        "description": "Write content to a file and return the absolute path.",
        "parameters": {
            "type": "object",
            "properties": {
                "content": {"type": "string"}
            },
            "required": ["content"],
            "additionalProperties": False
        },
        "strict": True
    }
}]

completion = client.chat.completions.create(
    model="gpt-4o",
    messages=[{"role": "user", "content": "What is the weather like in Berlin today?"}],
    tools=tools
)

tool_call = completion.choices[0].message.tool_calls[0]
print(tool_call)
args = json.loads(tool_call.function.arguments)

result = get_weather(args["latitude"], args["longitude"])
print(result)

messages = []

messages.append(completion.choices[0].message)  # append model's function call message
messages.append({
    "role": "tool",
    "tool_call_id": tool_call.id,
    "content": str(result)
})

completion_2 = client.chat.completions.create(
    model="gpt-4o",
    messages=messages,
    tools=tools,
)

print(completion_2.choices[0].message.content)

# Add the model's response to the messages
messages.append(completion_2.choices[0].message)

# ------------------------------------------------------------

# Ask to write the conversation to a file
messages.append({
    "role": "user",
    "content": "Please write this conversation to a file."
})

completion_3 = client.chat.completions.create(
    model="gpt-4o",
    messages=messages,
    tools=tools,
)

print(completion_3.choices[0].message)

# Execute the tool call if it's requesting to write to a file
if completion_3.choices[0].message.tool_calls:
    tool_call = completion_3.choices[0].message.tool_calls[0]
    args = json.loads(tool_call.function.arguments)
    
    if tool_call.function.name == "write_to_file":
        file_path = write_to_file(args["content"])
        print(f"Conversation written to: {file_path}")

