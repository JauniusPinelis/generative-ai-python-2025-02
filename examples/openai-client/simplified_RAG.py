import os
from pydantic import BaseModel
from openai import OpenAI
from dotenv import load_dotenv
from rich import print

load_dotenv()


client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),  # This is the default and can be omitted
)

information = "Jaunius Pinelis is a great developer and loves to code. Lives in Vilnius, Lithuania."

completion = client.chat.completions.create(
    model="gpt-4o-2024-08-06",
    messages=[
        {"role": "system", "content": "Extract the event information."},
        {"role": "system", "content": "This is information for you to work with: " + information},
        {"role": "user", "content": "Who is Jaunius Pinelis?"},
    ],
)

event = completion.choices[0].message
print(event)