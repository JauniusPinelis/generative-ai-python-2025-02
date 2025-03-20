import os
from google import genai
from google.genai import types
from rich import print

from dotenv import load_dotenv
load_dotenv()

gemini_api_key = os.getenv("GEMINI_API_KEY")

client = genai.Client(
        api_key=gemini_api_key
    )

with open("Stock_Open_close.PNG", "rb") as f:
    image = f.read()

response = client.models.generate_content(
    model="gemini-2.0-flash",
    contents=[
        types.Part.from_bytes(data=image, mime_type="image/png"),
        "Write a short and engaging blog post based on this picture.",
    ],
    
)

print(response.text)