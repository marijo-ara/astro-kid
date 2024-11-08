import requests
import json
from text_to_video.config.settings import settings

class GenerativeLanguageAPI:
    def __init__(self):
        self.api_key = settings.API_KEY
        self.endpoint = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-latest:generateContent"

    def generate_content(self, prompt_text):
        headers = {"Content-Type": "application/json"}
        params = {"key": self.api_key}
        data = {
            "contents": [
                {
                    "parts": [
                        {"text": prompt_text}
                    ]
                }
            ]
        }

        response = requests.post(self.endpoint, headers=headers, params=params, data=json.dumps(data))

        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"Error {response.status_code}: {response.text}")
