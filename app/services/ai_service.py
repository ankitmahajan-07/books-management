import httpx
from app.core.config import settings
from typing import Optional
import json


async def generate_summary(text: str, max_tokens: int = 256) -> str:
    """Generate a summary using Groq's Llama model."""
    
    if not text:
        return ""
    
    prompt = f"""
        You are an expert summarization system.

        Your task:
        - Read the provided content.
        - Produce a concise summary.
        - Response MUST be ONLY valid JSON.
        - No explanations. No extra text. No Markdown.
        - Format:
        {{
          "summary": "<3-4 line clean, readable summary>"
        }}

        Content to summarize:
        \"\"\" 
        {text}
        \"\"\"
    """

    payload = {
        "model": "llama-3.1-8b-instant",
        "messages": [
            {
                "role": "user",
                "content": prompt
            }
        ],
        "max_tokens": max_tokens,
        "temperature": 0.3
    }

    headers = {
        "Authorization": f"Bearer {settings.groq_api_key}",
        "Content-Type": "application/json"
    }

    async with httpx.AsyncClient(timeout=40) as client:
        resp = await client.post(settings.ai_model_endpoint, json=payload, headers=headers)
        resp.raise_for_status()

        data = resp.json()
        print("Groq response data:", data)
        # Groq follows OpenAI format
        content = data["choices"][0]["message"]["content"]
        json_content = json.loads(content)

        return json_content["summary"].strip()
