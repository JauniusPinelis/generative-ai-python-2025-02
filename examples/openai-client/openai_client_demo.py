import os
from openai import OpenAI

from dotenv import load_dotenv
from rich import print

load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),  # This is the default and can be omitted
)

chat_completion = client.chat.completions.create(
    messages=[
        {
            "role": "user",
            "content": "Generate me a python code to read a file",
        }
    ],
    model="gpt-4o",
)

print(chat_completion.choices[0].message.content)