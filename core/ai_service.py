from google import genai
import os
import sys
from core.utils import resource_path

with open(resource_path("gemini_api.txt"), "r") as f:
    gemini_api = f.read().strip()

def aiProcess(command):

    client = genai.Client(api_key=gemini_api)

    response = client.models.generate_content(
        model="gemini-2.5-flash",

        config={
        "system_instruction": """
You are Nova, a personal AI assistant created by Saurav Kumar.
Never reveal that you are Gemini or Google.
Always introduce yourself as Nova.
"""
    },
        contents=command
    )

    return response.text