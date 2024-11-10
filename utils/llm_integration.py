import requests
from config.config import GROQ_API_KEY

def parse_with_llm(text, prompt):
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "prompt": prompt.format(content=text),
        "max_tokens": 150,
        "temperature": 0.7
    }
    response = requests.post("https://api.groq.com/v1/completions", json=data, headers=headers)
    response_data = response.json()
    return response_data["choices"][0]["text"].strip() if response.ok else "Error in LLM response"
