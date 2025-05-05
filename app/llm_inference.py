import os
import re
from dotenv import load_dotenv
import streamlit as st

# Load environment variables
load_dotenv('secrets.env')

# Gemini 2.0 Flash inference
def run_gemini_flash(prompt):
    """
    Run inference with Gemini 2.0 Flash model.
    """
    try:
        from google import genai
        from google.genai import types
        
        # Create a client
        client = genai.Client(api_key=os.environ['GEMINI_API_KEY'])
        
        # Model configuration
        MODEL_ID = "gemini-2.0-flash"
        
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
        return f"Error with Gemini 2.0 Flash: {str(e)}"

# Gemini 2.5 Pro inference
def run_gemini_pro(prompt):
    """
    Run inference with Gemini 2.5 Pro model.
    """
    try:
        from google import genai
        from google.genai import types
        
        # Create a client
        client = genai.Client(api_key=os.environ['GEMINI_API_KEY'])
        
        # Model configuration
        MODEL_ID = "gemini-2.5-pro-exp-03-25"
        
        # Generate content
        contents = [
            types.Content(
                role="user",
                parts=[types.Part.from_text(text=prompt)],
            ),
        ]
        
        response_parts = []
        
        # Using streaming for potentially faster initial responses
        for chunk in client.models.generate_content_stream(
            model=MODEL_ID,
            contents=contents,
            config=types.GenerateContentConfig(
                temperature=0.4,
                response_mime_type="text/plain",
            ),
        ):
            response_parts.append(chunk.text if hasattr(chunk, 'text') else "")
        
        return "".join(response_parts)
    except Exception as e:
        return f"Error with Gemini 2.5 Pro: {str(e)}"

# Deepseek R1 via Together API inference
def run_deepseek_r1_together(prompt):
    """
    Run inference with Deepseek R1 model via Together API.
    """
    try:
        from huggingface_hub import InferenceClient
        
        # Create a client
        client = InferenceClient(
            provider="together",
            api_key=os.environ['TOGETHER_API_KEY']
        )
        
        # Prepare messages
        messages = [
            {
                "role": "user",
                "content": prompt
            }
        ]
        
        # Generate completion
        completion = client.chat.completions.create(
            model="deepseek-ai/DeepSeek-R1", 
            messages=messages, 
            max_tokens=4000,
            temperature=0.6
        )
        
        # Extract message content
        return completion.choices[0].message.content
    except Exception as e:
        return f"Error with Deepseek R1 (Together): {str(e)}"

# Llama 4 Scout via KlusterAI inference
def run_llama4_scout_klusterai(prompt):
    """
    Run inference with Llama 4 Scout model via KlusterAI.
    """
    try:
        from openai import OpenAI
        
        # Create a client with KlusterAI settings
        client = OpenAI(
            api_key=os.environ['KLUSTERAI_API_KEY'],
            base_url="https://api.kluster.ai/v1"
        )
        
        # Prepare messages
        messages = [
            {
                "role": "user",
                "content": prompt
            }
        ]
        
        # Generate completion
        completion = client.chat.completions.create(
            model="meta-llama/Llama-4-Scout-17B-16E-Instruct",
            max_completion_tokens=4000,
            temperature=0.6,
            top_p=1,
            messages=messages
        )
        
        # Try object attribute access first, fall back to dictionary access
        message = completion.choices[0].message
        content = getattr(message, 'content', None) or message.get('content')
        
        return content
    except Exception as e:
        return f"Error with Llama 4 Scout (KlusterAI): {str(e)}"

# Ollama Phi-4 Mini Reasoning inference

def run_ollama_phi4_mini_reasoning(prompt):
    """
    Run inference with Ollama phi4-mini-reasoning:latest model.
    """
    try:
        import ollama
        model = "phi4-mini-reasoning:latest"
        messages = [{"role": "user", "content": prompt}]
        response = ollama.chat(model=model, messages=messages)
        response_content = response['message']['content']
        def remove_thinking_tags(text):
            cleaned_text = re.sub(r'<think>.*?</think>', '', text, flags=re.DOTALL)
            return cleaned_text.strip()
        if '<think>' in response_content:
            response_content = remove_thinking_tags(response_content)
        return response_content
    except Exception as e:
        return f"Error with Ollama Phi-4 Mini Reasoning: {str(e)}"

# Ollama Mistral Small 3.1 inference

def run_ollama_mistral_small3(prompt):
    """
    Run inference with Ollama mistral-small3.1:24b-instruct-2503-q4_K_M model.
    """
    try:
        import ollama
        model = "mistral-small3.1:24b-instruct-2503-q4_K_M"
        messages = [{"role": "user", "content": prompt}]
        response = ollama.chat(model=model, messages=messages)
        response_content = response['message']['content']
        def remove_thinking_tags(text):
            cleaned_text = re.sub(r'<think>.*?</think>', '', text, flags=re.DOTALL)
            return cleaned_text.strip()
        if '<think>' in response_content:
            response_content = remove_thinking_tags(response_content)
        return response_content
    except Exception as e:
        return f"Error with Ollama Mistral Small 3.1: {str(e)}"

# Ollama Qwen3 14B inference

def run_ollama_qwen3(prompt):
    """
    Run inference with Ollama qwen3:14b model.
    """
    try:
        import ollama
        model = "qwen3:14b"
        messages = [{"role": "user", "content": prompt}]
        response = ollama.chat(model=model, messages=messages)
        response_content = response['message']['content']
        def remove_thinking_tags(text):
            cleaned_text = re.sub(r'<think>.*?</think>', '', text, flags=re.DOTALL)
            return cleaned_text.strip()
        if '<think>' in response_content:
            response_content = remove_thinking_tags(response_content)
        return response_content
    except Exception as e:
        return f"Error with Ollama Qwen3 14B: {str(e)}"