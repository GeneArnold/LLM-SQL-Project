import os
from dotenv import load_dotenv
from openai import OpenAI

# Load the API key from .env
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Make a simple call to test
response = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "What is 2 + 2?"}
    ]
)

print("✅ OpenAI response:", response.choices[0].message.content)