"""OpenAI client helpers for field extraction functions."""

from __future__ import annotations

import json
import os

from openai import OpenAI

# Load secrets from environment or .streamlit/secrets.toml (Streamlit macht das automatisch)
client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    organization=os.getenv("OPENAI_ORG"),
)


# Funktion für Option 1: Klassisches Function Calling
def call_extract_fields_function_calling(text, language="de"):
    function_def = {
        "name": "extract_job_fields",
        "description": "Extract structured job ad fields like title, skills, benefits, location.",
        "parameters": {
            "type": "object",
            "properties": {
                "text": {"type": "string", "description": "Job ad full text"},
                "language": {"type": "string", "enum": ["en", "de"]},
            },
            "required": ["text", "language"],
        },
    }
    try:
        response = client.chat.completions.create(
            model="gpt-4o",  # Alternativ: "gpt-4" oder "gpt-3.5-turbo"
            messages=[
                {
                    "role": "system",
                    "content": "You are an expert for extracting job ad data. Output strictly as function call.",
                },
                {
                    "role": "user",
                    "content": f"Extract all relevant job fields from this job ad: {text[:3000]}",
                },
            ],
            tools=[{"type": "function", "function": function_def}],
            tool_choice={
                "type": "function",
                "function": {"name": "extract_job_fields"},
            },
            temperature=0.2,
            max_tokens=1000,
        )
        tool_call = response.choices[0].message.tool_calls[0]
        arguments = tool_call.function.arguments if tool_call else "{}"
        return json.loads(arguments)
    except Exception as e:
        return {"error": str(e)}


# Funktion für Option 2: Responses API (Tool Loop)
def call_extract_fields_responses_api(text, language="de"):
    # Beispielhaftes Mockup – für echten Einsatz OpenAI Assistants API verwenden
    # Responses API ist (noch) nur mit HTTP-Requests oder openai.beta nutzbar (bald nativ in openai)
    # Hier ein Platzhalter-Call:
    # → In echt würdest du einen Thread anlegen, Tool(s) übergeben und Messages senden
    try:
        # Als Demo: Verwende die gleiche Extraktion wie oben (Simulation)
        # Für echte Integration siehe: https://platform.openai.com/docs/guides/function-calling?api-mode=responses
        return call_extract_fields_function_calling(text, language)
    except Exception as e:
        return {"error": str(e)}
