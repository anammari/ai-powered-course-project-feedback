from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv('secrets.env')

client = OpenAI(
  api_key = os.getenv('KLUSTERAI_API_KEY'),
  base_url = "https://api.kluster.ai/v1"
)

messages = [
    {
        "role": "user",
        "content": "What is the best cheese in France. Choose one."
    }
]

completion = client.chat.completions.create(
  model = "meta-llama/Llama-4-Scout-17B-16E-Instruct",
  max_completion_tokens = 4000,
  temperature = 0.6,
  top_p = 1,
  messages = messages
)

# Try object attribute access first, fall back to dictionary access
message = completion.choices[0].message
content = getattr(message, 'content', None) or message.get('content')
print(content)