"""
Gemeni-based project detector.

This module contains the GeminiDetector class that uses Gemini's API
for intelligent project analysis and tool detection.
"""

import os
from google import genai


if __name__ == "__main__":
    api_key = os.getenv("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)
    response = client.models.generate_content(
        model="gemini-2.5-flash", contents="I'm testing Gemini API with Python! Say hello!"
    )
    print(response.text)