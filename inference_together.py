from huggingface_hub import InferenceClient
from dotenv import load_dotenv
import os

load_dotenv('secrets.env')

client = InferenceClient(
    provider="together",
    api_key=os.getenv('TOGETHER_API_KEY')
)

messages = [
    {
        "role": "user",
        "content": "What is the best cheese in France. Choose one."
    }
]

completion = client.chat.completions.create(
    model="deepseek-ai/DeepSeek-R1", 
    messages=messages, 
    max_tokens=2048
)

print(completion.choices[0].message)
