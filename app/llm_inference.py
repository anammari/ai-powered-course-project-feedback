import os
import re
from dotenv import load_dotenv
import streamlit as st

# Load environment variables
load_dotenv('secrets.env')

# Gemini 2.5 Flash inference
def run_gemini_flash(prompt):
    """
    Run inference with Gemini 2.5 Flash model.
    """
    try:
        from google import genai
        from google.genai import types
        
        # Create a client
        client = genai.Client(api_key=os.environ['GEMINI_API_KEY'])
        
        # Model configuration
        MODEL_ID = "gemini-2.5-flash"
        
        # Generate content
        response = client.models.generate_content(
            model=MODEL_ID,
            contents=prompt,
            config=types.GenerateContentConfig(
                temperature=0.4,
                top_p=0.95,
                top_k=20,
                candidate_count=1,
                max_output_tokens=4000,
            )
        )
        
        return response.text
    except Exception as e:
        return f"Error with Gemini 2.5 Flash: {str(e)}"

# GPT-OSS 120B via Together API inference
def run_deepseek_r1_together(prompt):
    """
    Run inference with GPT-OSS 120B model via Together API.
    """
    try:
        from together import Together
        
        client = Together()
        
        response = client.chat.completions.create(
            model="openai/gpt-oss-120b",
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )
        
        return response.choices[0].message.content
    except Exception as e:
        return f"Error with GPT-OSS 120B (Together): {str(e)}"

# Ollama GPT-OSS inference

def run_ollama_gpt_oss(prompt):
    """
    Run inference with Ollama gpt-oss:20b model.
    """
    try:
        from ollama import chat
        
        response = chat(model='gpt-oss:20b', messages=[
            {
                'role': 'user',
                'content': prompt,
            },
        ])
        
        response_content = response['message']['content']
        def remove_thinking_tags(text):
            cleaned_text = re.sub(r'<think>.*?</think>', '', text, flags=re.DOTALL)
            return cleaned_text.strip()
        if '<think>' in response_content:
            response_content = remove_thinking_tags(response_content)
        return response_content
    except Exception as e:
        return f"Error with Ollama GPT-OSS 20B: {str(e)}"
