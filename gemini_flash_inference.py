from google import genai
from google.genai import types
import os
from dotenv import load_dotenv, find_dotenv

# Load environment variables
load_dotenv('secrets.env')

# Suppress logging warnings
os.environ["GRPC_VERBOSITY"] = "ERROR"
os.environ["GLOG_minloglevel"] = "2"

# Ensure the API key is set correctly
GOOGLE_API_KEY = os.getenv('GEMINI_API_KEY')
os.environ["GOOGLE_API_KEY"] = GOOGLE_API_KEY
os.environ["GEMINI_API_KEY"] = GOOGLE_API_KEY

# Create a client
client = genai.Client(api_key=os.environ['GEMINI_API_KEY'])

MODEL_ID =  "gemini-2.0-flash"  #"gemini-2.5-pro-exp-03-25"

response = client.models.generate_content(
    model=MODEL_ID,
    contents="Tell me how the internet works, but pretend I'm a puppy who only understands squeaky toys.",
    config=types.GenerateContentConfig(
        temperature=0.4,
        top_p=0.95,
        top_k=20,
        candidate_count=1,
        seed=5,
        max_output_tokens=500,
        stop_sequences=["STOP!"],
        presence_penalty=0.0,
        frequency_penalty=0.0,
    )
)

print(response.text)