from rich import print
import os 
from dotenv import load_dotenv
import requests
import json
import google.generativeai as genai
from google.generativeai.types import FunctionDeclaration, Tool

load_dotenv()

google_api_key = os.getenv("GEMINI_API_KEY")
if google_api_key is None:
    print("Please set GOOGLE_API_KEY in .env file")
    exit(1)

# Configure the Gemini API
genai.configure(api_key=google_api_key)

def get_weather(latitude: str, longitude: str):
    response = requests.get(f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&current=temperature_2m,wind_speed_10m&hourly=temperature_2m,relative_humidity_2m,wind_speed_10m")
    data = response.json()
    return data['current']['temperature_2m']

def write_to_file(content: str, filename: str = "output.txt"):
    with open(filename, 'w') as file:
        file.write(content)
    return os.path.abspath(filename)

# Define the tools for Gemini
weather_tool = Tool(
    function_declarations=[
        FunctionDeclaration(
            name="get_weather",
            description="Get current temperature for provided coordinates in celsius.",
            parameters={
                "type": "object",
                "properties": {
                    "latitude": {"type": "number"},
                    "longitude": {"type": "number"}
                },
                "required": ["latitude", "longitude"]
            }
        )
    ]
)

file_tool = Tool(
    function_declarations=[
        FunctionDeclaration(
            name="write_to_file",
            description="Write content to a file and return the absolute path.",
            parameters={
                "type": "object",
                "properties": {
                    "content": {"type": "string"}
                },
                "required": ["content"]
            }
        )
    ]
)

# Initialize Gemini model with tools
model = genai.GenerativeModel(
    model_name="gemini-1.5-pro",
    tools=[weather_tool, file_tool],
    generation_config={"temperature": 0.4}
)

chat = model.start_chat()

# Ask about the weather
response = chat.send_message("What is the weather like in Berlin today?")
print(response.candidates[0].content)

# Process the function call
function_call = response.candidates[0].content.parts[0].function_call
print(function_call)

if function_call.name == "get_weather":
    # Extract arguments
    args = function_call.args
    latitude = args["latitude"]
    longitude = args["longitude"]
    
    # Call the weather function
    result = get_weather(latitude, longitude)
    
    # Send the function result back to the model
    function_response = chat.send_message(
        {"function_response": {
            "name": "get_weather",
            "response": {"temperature": result}
        }}
    )
    print(function_response.text)

# # Ask to write the conversation to a file
# file_request = chat.send_message("Please write this conversation to a file.")
# print(file_request.candidates[0].content)

# # Process the function call for file writing
# if hasattr(file_request.candidates[0].content.parts[0], 'function_call'):
#     function_call = file_request.candidates[0].content.parts[0].function_call
    
#     if function_call.name == "write_to_file":
#         content = function_call.args["content"]
#         file_path = write_to_file(content)
        
#         # Send function result back to model
#         chat.send_message(
#             {"function_response": {
#                 "name": "write_to_file",
#                 "response": {"file_path": file_path}
#             }}
#         )
#         print(f"Conversation written to: {file_path}")