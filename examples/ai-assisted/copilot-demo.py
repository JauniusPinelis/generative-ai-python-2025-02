import openai
from dotenv import load_dotenv
import os

# Replace 'your-api-key' with your actual OpenAI API key
load_dotenv(os.path.join(os.path.dirname(__file__), '..', '.env'))
openai.api_key = os.getenv('OPENAI_API_KEY')

def get_completion(prompt):
    response = openai.Completion.create(
        engine="gpt-4",
        prompt=prompt
    )
    return response.choices[0].text.strip()

def main():
    user_prompt = input("Enter a prompt: ")
    completion = get_completion(user_prompt)
    print("Completion:", completion)

if __name__ == "__main__":
    main()
